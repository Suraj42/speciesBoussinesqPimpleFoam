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

#include "initExpField.H"
#include "Time.H"
#include "fvMesh.H"
#include "addToRunTimeSelectionTable.H"
#include "vector.H"
#include "fvCFD.H"

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

namespace Foam
{
namespace functionObjects
{
    defineTypeNameAndDebug(initExpField, 0);
    addToRunTimeSelectionTable(functionObject, initExpField, dictionary);
}
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::functionObjects::initExpField::initExpField
(
    const word& name,
    const Time& runTime,
    const dictionary& dict
)
:
    fvMeshFunctionObject(name, runTime, dict),
    time_(runTime),
    mesh_(time_.lookupObject < fvMesh > (polyMesh::defaultRegion))
{
    read(dict);
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //
std::vector<double> readCSVColumn(const std::string& filePath, int columnIndex)
{
    std::vector<double> columnValues;

    std::ifstream file(filePath);
    if (file.is_open())
    {
        std::string line;
        while (std::getline(file, line))
        {
            std::istringstream iss(line);
            std::string valueStr;

            // Loop through the values in the line until reaching the desired column
            for (int i = 0; i <= columnIndex; ++i)
            {
                if (!std::getline(iss, valueStr, ','))
                {
                    // Invalid column index
                    file.close();
                    return columnValues;
                }
            }

            double value = std::stod(valueStr);
            columnValues.push_back(value);
        }
        file.close();
    }
    else
    {
        std::cerr << "Error: Unable to open file " << filePath << std::endl;
    }

    return columnValues;
}

void Foam::functionObjects::initExpField::setExpField()
{   
    Info << "Running FO initialiseField to set experimental field" << endl;
    Info << " " << endl;
    
    // Get the list of labels of cells in the cell Zone
    const auto& cells = mesh_.cellCentres();

    // Get the concentration field as a scalar field to set experimental values
    auto& c_ = mesh_.lookupObjectRef<volScalarField>("C");

    //const auto& cIF = mesh_.C();

    // Specify the path to the CSV file
    // std::string filePath = "constant/fieldValuesCellZone.csv";
     std::string filePath = "constant/initialFieldValues.csv";
    // Specify the column index (zero-based)
    int columnIndex = 0;  

    // Read the column of values from the CSV file
    std::vector<double> columnValues = readCSVColumn(filePath, columnIndex);

    //auto& c_  = const_cast<Foam::scalarField&> (mesh_.lookupObjectRef<scalarField>("C"));

    // Loop over all the cells in cell zone and assign experimental field value
    forAll(cells, cellI)
    {
        //const label cell = cells[cellI];
        c_[cellI] = columnValues[cellI];
        //Info << cIF[cell] << endl;
        //Info << cell << endl;
    }
    Info << "Done setting experimental field values in a 11 X 11 mm cellZone" << endl;
    Info << " " << endl;
    
}
bool Foam::functionObjects::initExpField::read(const dictionary& dict)
{
    setExpField();
    return true;
}


bool Foam::functionObjects::initExpField::execute()
{
    return true;
}


bool Foam::functionObjects::initExpField::end()
{
    return true;
}


bool Foam::functionObjects::initExpField::write()
{
    return true;
}


// ************************************************************************* //
