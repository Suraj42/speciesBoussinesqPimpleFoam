/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2023 AUTHOR, AFFILIATION
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

Class
    Foam::functionObjects::evaluateFlux_lowH

Group
    grpFieldFunctionObjects

Description
    <minimal description of the function object>

    <equation>
    \f[
        x = x_{ref}^x + \rho \omega
    \f]

    <variable-explanation table>
    where
    \vartable
      \rho        | <explanation> [units, e.g. kg/m3]
      \omega      | \f$ \nabla \cdot \vec U \f$
      ...         | ...
    \endvartable

    <inline equation>
    where \f$ x_k \f$ is ...

    <input-output table>
    \table
      Operand      | Type                 | Location
      input        | {vol,surface}\<Type\>Field(s) <!--
               --> |$FOAM_CASE/\<time\>/\<inpField\>s
      output file  | dat                  <!--
              -->  | $FOAM_CASE/postProcessing/\<FO\>/\<time\>/\<file\>
      output field | volScalarField       | $FOAM_CASE/\<time\>/\<outField\>
    \endtable

Usage
    Minimal example by using \c system/controlDict.functions:
    \verbatim
    evaluateFlux1
    {
        // Mandatory entries (unmodifiable)
        type           evaluateFlux_lowH;
        libs           (evaluateFluxFunctionObject);

        // Mandatory entries (runtime modifiable)
        ...

        // Mandatory (inherited) entries (unmodifiable)
        ...

        // Mandatory (inherited) entries (runtime unmodifiable)
        ...

        // Optional entries (unmodifiable)
        ...

        // Optional entries (runtime modifiable)
        boolData       <bool>;
        labelData      <label>;
        wordData       <word>;
        scalarData     <scalar>;

        // Optional (inherited) entries
        ...
    }
    \endverbatim

    where the entries mean:
    \table
      Property   | Description                      | Type | Req'd | Dflt
      type       | Type name: evaluateFlux_lowH        | word |  yes  | -
      libs       | Library name: evaluateFluxFunctionObject  <!--
             --> | word  | yes | -
      boolData   | <explanation>                    | bool |  yes  | -
      labelData  | <explanation>                    | label |  yes | -
      wordData   | <explanation>                    | word |  yes  | -
      scalarData | <explanation>                    | scalar |  no | 1.0
      wordListData  | <explanation>                 | wordList | yes | -
    \endtable

    Options for the \c ENTRY entry:
    \verbatim
        <option1>
        <option2> | <explanation>
      ...
    \endverbatim

    The inherited entries are elaborated in:
     - \link functionObject.H \endlink
     - \link fieldExpression.H \endlink
     - \link fieldsExpression.H \endlink
     - \link writeFile.H \endlink
     ...

    <if \c postProcess is applicable>
    Minimal example by using the \c postProcess utility:
    \verbatim
        postProcess -func evaluateFlux_lowH
    \endverbatim

    <if \c postProcess is not applicable>
    Usage by the \c postProcess utility is not available.

Note
    - <note1>
    - <note2>
    ...

See also
    - Foam::functionObject
    - Foam::functionObjects::fvMeshFunctionObject
    - ExtendedCodeGuide::functionObjects::field::evaluateFlux_lowH
    ...

SourceFiles
    evaluateFlux_lowH.C
    evaluateFluxTEMPLATES.C
    ...

\*---------------------------------------------------------------------------*/

#ifndef evaluateFluxCH_H
#define evaluateFluxCH_H
#include "volFields.H"
#include "fvMeshFunctionObject.H"
#include "OFstream.H"
#include "fvMesh.H"
#include "Time.H"
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{
namespace functionObjects
{

/*---------------------------------------------------------------------------*\
                   Class evaluateFlux_lowH Declaration
\*---------------------------------------------------------------------------*/

class evaluateFlux_lowH
:
    public fvMeshFunctionObject
{
    // Private Data
    //-Time
    const Time & time_;

    //- Mesh const reference.
    const fvMesh & mesh_;

    // Output file for writing
    OFstream outputFile;  

    protected:

        //- Transport properties dict
        const IOdictionary transPropDict_;
        // Diffusion coeff.
        const dimensionedScalar D_;
        // Henry coeff. 
        double H_;
        // Universal gas constant
        const double R_;
        // Ambient temperature during expriment
        const double T_ ; 
        // Saturation pressure at T
        const double p_e_sat_;
        // number of moles of ethanol
        double n_e_l_;
        // number of moles of ethylene glycol
        double n_eg_0_;
        // Film wdith
        const double filmWidth_;
        // Film length
        const double filmLength_;
        // Film wdith
        const double filmThickness_;
        // Get the patch id of the interface/ drop
        const label patchId_;
        // Get the interface patch cell length provided uniform meh size
        scalar iCellLength_;

public:

    //- Runtime type information
    TypeName("evaluateFlux_lowH");

    // Constructors

        //- Construct from Time and dictionary
        evaluateFlux_lowH
        (
            const word& name,
            const Time& runTime,
            const dictionary& dict
        );

        //- No copy construct
        evaluateFlux_lowH(const evaluateFlux_lowH&) = delete;

        //- No copy assignment
        void operator=(const evaluateFlux_lowH&) = delete;


    //- Destructor
    virtual ~evaluateFlux_lowH() = default;


    // Member Functions

        // Calculate the flux for each time step
        virtual void calculateConcInTime();

        // Calculate the initial flux and c_e_g
        virtual void calculateInitConc();

        //- Read the evaluateFlux_lowH data
        virtual bool read(const dictionary& dict);

        //- Execute, currently does nothing
        virtual bool execute();

        //- Execute at the final time-loop, currently does nothing
        virtual bool end();

        //- Write the evaluateFlux_lowH
        virtual bool write();
};


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace functionObjects
} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //
