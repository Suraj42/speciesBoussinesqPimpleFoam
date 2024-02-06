#### Plot:
plt.figure()
# NOTE: Scale for values is selcted by hand currently! The boundary region is
# avoided by using ylim.
plt.pcolormesh(Xi, Yi, diffusion_flux_divergence, cmap = 'viridis_r', vmin=-1,vmax=1)
plt.colorbar()
plt.title("Divergence of diffusion flux")
plt.ylim([0.002,0.01])
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig("divergence_diffusion_flux.pdf")

#### Plot:
plt.figure()
# NOTE: Scale for values is selcted by hand currently! The boundary region is
# avoided by using ylim.
plt.pcolormesh(Xi, Yi, convective_flux_divergence, cmap = 'viridis_r', vmin=-1,vmax=1)
plt.colorbar()
plt.title("Divergence of convective flux")
plt.ylim([0.002,0.01])
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig("divergence_convective_flux.pdf")

#### Plot:
plt.figure()
# NOTE: Scale for values is selcted by hand currently! The boundary region is
# avoided by using ylim.
plt.pcolormesh(Xi, Yi, total_flux_divergence, cmap = 'viridis_r', vmin=-1,vmax=1)
plt.colorbar()
plt.title("Divergence of total flux")
plt.ylim([0.002,0.01])
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig("divergence_total_flux.pdf")

#### Plot:
plt.figure()
plt.pcolormesh(Xi, Yi, np.log(abs(U_divergence)), cmap = 'viridis_r')
plt.colorbar()
plt.title("Log|Divergence of Velocity field|")
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig("divergence_velocity.pdf")
