fvVectorMatrix UEqn
(
    fvm::ddt(U) + fvm::div(phi, U)
    - fvm::laplacian(nu, U)
);

UEqn.relax();

if (pimple.momentumPredictor()) 
{
    solve
    (
        UEqn
     ==
        fvc::reconstruct
        (
            (
              - ghf* fvc::snGrad(rhok) 
              - fvc::snGrad(p_rgh)
            )*mesh.magSf()
        )
    );

    fvOptions.correct(U);
}
