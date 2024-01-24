//Info<< "Reading thermophysical properties\n" << endl;

Info << "Reading field C\n" << endl;
volScalarField C
(
    IOobject
    (
        "C",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info << "Reading field p_rgh\n" << endl;
volScalarField p_rgh
(
    IOobject
    (
        "p_rgh",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info << "Reading field U\n" << endl;
volVectorField U
(
    IOobject
    (
        "U",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info << "Reading/calculating face flux field phi\n" << endl;

surfaceScalarField phi
(
    IOobject
    (
        "phi",
        runTime.timeName(),
        mesh,
        IOobject::READ_IF_PRESENT,
        IOobject::AUTO_WRITE
    ),
    fvc::flux(U) 
);


IOdictionary transportProperties
(
    IOobject
    (
        "transportProperties",
        runTime.constant(),
        mesh,
        IOobject::MUST_READ,
        IOobject::NO_WRITE
    )
);

// read constant/transportProperties
const dimensionSet dimConcentration(0, -3, 0, 0, 1, 0, 0);
const dimensionedScalar nu("nu", dimensionSet(0, 2, -1, 0, 0, 0 ,0), transportProperties);
const dimensionedScalar D("D", dimensionSet(0, 2, -1, 0, 0, 0 ,0), transportProperties);
const dimensionedScalar Cs("Cs", dimConcentration, transportProperties);
const dimensionedScalar rho_0("rho_0", dimDensity, transportProperties);
const dimensionedScalar drho("drho", dimDensity, transportProperties);

const dimensionedScalar dMolarMass("dMolarMass", dimensionSet(1, 0, 0, 0, -1, 0 ,0), transportProperties);

volScalarField rhok
(
    IOobject
    (
        "rhok",
        runTime.timeName(),
        mesh,
        IOobject::READ_IF_PRESENT,
        IOobject::AUTO_WRITE
    ),
    1.0 + ((dMolarMass*C)/rho_0)
);

Info << "\nReading g" << endl;
const meshObjects::gravity& g = meshObjects::gravity::New(runTime);

Info << "\nReading hRef" << endl;
uniformDimensionedScalarField hRef
(
    IOobject
    (
        "hRef",
        runTime.constant(),
        mesh,
        IOobject::READ_IF_PRESENT,
        IOobject::NO_WRITE
    ),
    dimensionedScalar(dimLength, Zero)
); // just a zero if it is not read

Info << "Calculating field g.h\n" << endl;
dimensionedScalar ghRef
(
    mag(g.value()) > SMALL
  ? g & (cmptMag(g.value())/mag(g.value()))*hRef
  : dimensionedScalar("ghRef", g.dimensions()*dimLength, 0)
);// this means that ghRef is zero if hRef-file is not present
volScalarField gh("gh", (g & mesh.C()) - ghRef); 
surfaceScalarField ghf("ghf", (g & mesh.Cf()) - ghRef);


volScalarField p // this is p_mod
(
    IOobject
    (
        "p",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    p_rgh + rhok*gh 
);

label pRefCell = 0;
scalar pRefValue = 0.0;

setRefCell
(
    p,
    p_rgh,
    pimple.dict(),
    pRefCell,
    pRefValue
);


if (p_rgh.needReference())  
{
    p += dimensionedScalar
    (
        "p",
        p.dimensions(),
        pRefValue - getRefCellValue(p, pRefCell)
    );
    
}

mesh.setFluxRequired(p_rgh.name()); 

// without this, the constrainPressure function can not be called
IOMRFZoneList MRF(mesh); // from #include createMRF.H

fv::options& fvOptions(fv::options::New(mesh));
if (!fvOptions.optionList::size())
{
    Info << "No finite volume options present" << endl;
}
