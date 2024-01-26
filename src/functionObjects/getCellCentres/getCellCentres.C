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

#include "argList.H"
#include "Time.H"
#include "fvMesh.H"
//#include "addToRunTimeSelectionTable.H"
#include "vector.H"
#include "fvCFD.H"
#include "volFields.H"
#include "OFstream.H"

using namespace Foam;

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
 
    // #include "addCheckCaseOptions.H"
    #include "setRootCase.H"
    #include "createTime.H"
    //#include "createMesh.H"
    #include "createControl.H"
    #include "createPolyMesh.H"

    Info << "Running utility to write all cells into a csv file" << endl;
    Info << " " << endl;

    const std::string fileName("cellCentres.csv");
    std::ofstream cellsFile(fileName, std::ios::out);
    cellsFile << "x, y, z" << std::endl;

    // Get the list of labels of cells in the cell Zone
    const auto& cells = mesh.cells();

    const auto& cIF = mesh.cellCentres();

    // Loop over all the cells in cell zone and assign experimental field value
    forAll(cells, cellI)
    {
        //const label cell = cells[i];
        cellsFile << cIF[cellI][0] << ", "
                << cIF[cellI][1] << ", "
                << cIF[cellI][2] << nl;
        //Info << cIF[cell] << endl;
        //Info << cell << endl;
    }
    Info << "Done writing cells into file for interpolation in py script" << endl;
    Info << " " << endl;

    return 0;
}