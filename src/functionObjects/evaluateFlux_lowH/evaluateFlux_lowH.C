/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2023 AUTHOR,AFFILIATION
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "evaluateFlux_lowH.H"
#include <memory>
#include "fvCFD.H"
#include "addToRunTimeSelectionTable.H"
#include "surfaceFieldsFwd.H"
#include "vectorList.H"
#include <list>
#include <cmath>

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

namespace Foam
{
namespace functionObjects
{
    defineTypeNameAndDebug(evaluateFlux_lowH, 0);
    addToRunTimeSelectionTable(functionObject, evaluateFlux_lowH, dictionary);
}
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::functionObjects::evaluateFlux_lowH::evaluateFlux_lowH
(
    const word& name,
    const Time& runTime,
    const dictionary& dict
)
:
    fvMeshFunctionObject(name, runTime, dict),
    time_(runTime),
    mesh_(time_.lookupObject < fvMesh > (polyMesh::defaultRegion)), 
    outputFile("flux_drop.csv"),
    transPropDict_ 
    (
        IOobject
        (
            "transportProperties",
            "constant",
            mesh_.time(), 
            IOobject::MUST_READ,
            IOobject::NO_WRITE
        )
    ),
    D_(dimensionedScalar("D", dimViscosity ,transPropDict_)),
    H_(-1), // Henry coeffcient to be set later
    R_(8.3144), // Universal gas constant in SI units
    T_(300.28), // Ambient temperature during expriment in Kelvin
    p_e_sat_(8895.0), // Saturation pressure at T of pure ethanol in Pascal
    n_e_l_(-1), // number of moles of ethanol in liquid, decreasing with time
    n_eg_0_(-1), // number of moles of ethelene glycol in liquid, Assumed ocnstant
    filmWidth_(0.003), // Film wdith in metre
    filmLength_(0.060), // Film length in metre
    filmThickness_(50E-06), // Film thickness in metre
    patchId_(mesh_.boundaryMesh().findPatchID("drop")),  // Get the patch ID of the interface patch
    iCellLength_(-1) // Get the interface patch cell length, provided uniform mesh
    { 
        outputFile << "t(in s), flux (mol/ms), n_e_l(t)(mol), c_e_g(t)(mol/m3)\n";
        read(dict);
    }

// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //
void Foam::functionObjects::evaluateFlux_lowH::calculateInitConc()
{
    Info << "Running initial concentration caluclation in the FO evaluateFlux_lowH" << endl;
    Info << " " << endl;
    // set Henry coefficient
    H_ = 0.926462; 
    Info << "constant H: " << H_ << endl;
    Info << "D " << D_.value() << endl;

    auto c_ = mesh_.lookupObjectRef<volScalarField>("C");

    //  area = width * length
    const double filmArea = filmWidth_ * filmLength_;

    // volume of the film
    const double v_0 = filmThickness_ * filmArea ;
    Info << "v_0: " << v_0 << endl;

    // Lambda constant, y_e * rho_eg / y_eg * rho_e
    const double lambda_0 = (0.3 * 1115) / (0.7 * 789);
    Info << "lambda_0: " << lambda_0 << endl;

    const double preFactor = 0.70;
    // initial molar mass of ethanol, 0.6*rho_e*lambda* v_0/ (1+lambda)* Molar mass of e
    const double n_e_0 = (preFactor*789*lambda_0*v_0) / ((1+lambda_0)*0.0461) ;
    Info << "n_e_0: " << n_e_0 << endl;

    // initial molar mass of ethanol, rho_eg* v_0/ (1+lambda)* Molar mass of eg
    n_eg_0_ = (1115*v_0) / ((1+lambda_0)*0.0621) ;
    Info << "n_eg_0: " << n_eg_0_ << endl;
    
    // Initial molar fraction
    const double x_e_l0 = n_e_0 / (n_e_0 + n_eg_0_) ;
    Info << "x_e_l(0) " << x_e_l0 << endl;

    // Calculate the conc. of ethanol on interface in the gas phase
    const auto c_e_gas_init = (p_e_sat_ / (R_ * T_)) * H_ * (n_e_0 / (n_eg_0_ + n_e_0) ) ;
    Info << "c_e_gas(0) " << c_e_gas_init << endl;

    // Get the interface patch to loop over its faces and assign the 
    // initial gas conc. value to the interface  
    const auto& interfacePatch = mesh_.boundary()[patchId_];

    forAll(interfacePatch,faceI)
    {
        c_.boundaryFieldRef()[patchId_][faceI] = c_e_gas_init; 
    }
    
    // Set the number of moles of ethanol that will change with time 
    // in liquid to initial number of moles of ethanol in liquid
    n_e_l_ = n_e_0 ;

    // Set the interface cell length 
    iCellLength_ = interfacePatch.Cf()[1][0] - interfacePatch.Cf()[0][0];
}
void Foam::functionObjects::evaluateFlux_lowH::calculateConcInTime()
{
    Info << "Running flux and concentration caluclation in the FO evaluateFlux_lowH" << endl;

    auto& c_ = mesh_.lookupObjectRef<volScalarField>("C");

    auto& C_ = mesh_.boundary()[patchId_].lookupPatchField<volScalarField,scalar>("C");
    Info << "C_ before: " << C_ << endl;

    // Get the area of faces in patch
    //const auto magSf = mesh_.magSf().boundaryField()[patchId];
    const auto magSf = mesh_.boundary()[patchId_].magSf();

    // Calculate the surface normal gradients of each face in the patch
    const auto snGradC = c_.boundaryField()[patchId_].snGrad();
    Info << "snGrad: " << c_.boundaryField()[patchId_].snGrad() << endl;

    // Get the interface patch
    const auto& interfacePatch = mesh_.boundary()[patchId_];
    //const label& startFace = interfacePatch.start();

    // Calculate the fluxes of each face in the patch, according to fick's law
    const tmp<scalarField> tFieldFlux = D_.value() * snGradC * iCellLength_; 
    //Info << "tFieldFlux: " << tFieldFlux << endl;

    // Flux through the entire 3mm patch
    const auto patchFlux = gSum(tFieldFlux()); 
    Info << "patchFlux: " << patchFlux << endl;

    // The flux through the patch integrated in time
    const auto delta_n_e_l = patchFlux * filmLength_ * time_.deltaT().value(); 
    Info << "delta_n_e_l: " << delta_n_e_l << endl;

    // *** Calculate the reduced  molar mass due to 
    //mass flux out of the patch as in eqn.  in paper
    n_e_l_ = n_e_l_ - delta_n_e_l; 
    Info << "n_e_l " << n_e_l_ << endl;

    // molar fraction in time
    const double x_e_l = n_e_l_ / (n_e_l_ + n_eg_0_) ;
    Info << "x_e_l(t) " << x_e_l << endl;

    Info << "H " << H_ << endl;

    // Calculate the conc. of ethanol on interface in the gas phase
    const auto c_e_gas = (p_e_sat_ / (R_ * T_)) * H_ * (n_e_l_ / (n_eg_0_ + n_e_l_ ) ) ;
    Info << "c_e_gas " << c_e_gas << endl;

    // Get the interface patch to loop over its faces and assign the 
    // reduced conc. value for the next time step
    forAll(interfacePatch,faceI)
    {
         c_.boundaryFieldRef()[patchId_][faceI] = c_e_gas;
    }
    
    Info << "C_after: " << C_ << endl;
 
    if( Pstream::master() ) // time_.writeTime() &&
    {
        outputFile << time_.timeOutputValue() << ", " 
                    << patchFlux << ", "  
                    << n_e_l_ << ", " 
                    << c_e_gas <<  endl; 
    }
    
}

bool Foam::functionObjects::evaluateFlux_lowH::read(const dictionary& dict)
{
    calculateInitConc();
    return true;
}


bool Foam::functionObjects::evaluateFlux_lowH::execute()
{
    calculateConcInTime();
    return true;
}


bool Foam::functionObjects::evaluateFlux_lowH::end()
{
    return true;
}


bool Foam::functionObjects::evaluateFlux_lowH::write()
{
    return true;
}


// ************************************************************************* //
