# ocean-wave-spectrum-parameterizations
Data and files accompanying Williams H.H. et al., "Observations and empirical functions for the ocean surface wave spectrum". 

File descriptions: LIDAR data comparison
- 
Compare ocean wave spectrum parameterizations to experimental data in a range of sea states

### compare_spectra.ipynb
Main notebook that generates plots to compare the three spectrum parameterizations to the experimental data.


### equilibrium.py, jonswap.py, piersonMoskowitz.py
Contain python classes for the three spectrum parameterizations: Equilibrium, JONSWAP, and Pierson-Moskowitz. Each is initialized in a slightly different way.


### lidData.py
Contains a class description for experimental data. Extracts the peak wavenumber $k_p$ and significant wave height $H_s$ based on the provided data and calculates the inputs for each spectrum parameterization accordingly.


### experimental_data/
Contains pickle (.pkl) files with data analyzed from SoCal2013, HiRes 2010, GOTEX, and ASIT TKE field campaigns. Each pickle contains a pandas dataframe with the associated data.

| Dataset         | File name                  | Variables      |
| --------------- | -------------------------- | ---------------------------  | 
| SoCal2013       | lenain.pkl                 | $k$, $\phi(k)$, $k_n$        |
| HiRes 2010      | pizzo.pkl                  | $k$, $\phi(k)$, $u_*$, $k_n$ |
| GOTEX           | romero_2010/romero_[].pkl  | $k$, $\phi(k)$, $u_*$, $X_e$, $U_{10}$ |
| ASIT TKE        | hogan_2025/hogan_[].pkl    | $k$, $\phi(k)$, $u_*$, $U_{10}$, $\theta_{wind}$, $k_n$|


File descriptions: LES analysis
- 
Post-processing for Large Eddy Simulations of Marine Atmospheric Boundary Layers sweeping wind and wave parameters


### les_mabl_comp.ipynb
Main notebook to analyze drag at the air-sea interface LES.

### les_helpers.py
Contains helper functions for plotting.

### stat_data.py
Class definition to read statistical data from LES (profiles averaged in time and space), calculated momentum fluxes, interpolate quantities at specific heights, etc.

### les_data
Directory containing data output from LES. Each file is named according to the wind and wave conditions for that run:
- $U_{bulk}$ (12, 18, or 24 m/s)
- $H_s$ (0.4, 1.2, or 2.0 m)
- $k_p$ (0.0393, 0.0785, or 0.157 m$^{-1}$)
- the spectrum parameterization:
    - no label or 'swell' for Equilibrium spectrum
    - 'js' for JONSWAP using the algorithm from Hasselmann et al. (1973)
    - 'js_match' for JONSWAP with matched energy