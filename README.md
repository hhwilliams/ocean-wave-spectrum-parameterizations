# ocean-wave-spectrum-parameterizations
Data and files to compare ocean wave spectrum parameterizations to experimental data in a range of sea states

File descriptions
- 
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
| ASIT TKE.       | hogan_2025/hogan_[].pkl    | $k$, $\phi(k)$, $u_*$, $U_{10}$, $\theta_{wind}$, $k_n$|


