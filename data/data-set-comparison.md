- Hagmann et al.:
  - 66 areas total
  - atlas: Desikan-Killiany-ish. Fischl et al. (2004)
  - cortical only
  - 5 participants (participant data is available online, not just averaged data)
  - DSI (others are DTI)

- Finger et al.:
  - 66 areas total (slightly different from Hagmann et al.)
  - Desikan-Killiany atlas; 'gyral based ROIs'; https://doi.org/10.1016/j.neuroimage.2006.01.021
  - cortical only
  - 17 participants

- NKI Rockland:
  - 188 areas
    - 'only' 95 ones are uniquely named, which is what's important when mapping to ACT-R areas
    - most of these are left/right hemispheric versions of the same thing, so actual identification is required for about half. Still some work, but possible
  - atlas by Craddock et al., based on fMRI data (not underlying structure!): https://www.ncbi.nlm.nih.gov/pubmed/21769991
  - quite complete: thalamus, hippocampus, etc.
  - plenty of participants
    - age & sex are known, health not. But chances of neurological problems are like in a normal population, so probably acceptable.
    - http://fcon_1000.projects.nitrc.org/indi/enhanced/access.html / http://fcon_1000.projects.nitrc.org/indi/pro/nki.html

- ICBM: UCLA_ICBM_1004_DTI
  - very similar mappings to Hagmann et al./Finger et al. for cortex (less work to relabel)
  - thalamus, hippocampus among other additional areas
  - single person data
  - related study unknown

- CCHMC_Hydro: CC03_70_00_62
  - 62 regions, including thalamus & hippocampus
  - atlas unknown
  - related study unknown
  - might not be adult data? (CCHMC = Cincinnati Children's Hospital Medical Center?; no age data)
  - probably averaged (gender set to mixed)

- WU-Minn HCP
  - as far as I can see, this data is not processed enough (no structural connectivity matrices)
    - functional connectivity matrices are there, I think, but that's useless.
    - https://mrtrix.readthedocs.io/en/latest/quantitative_structural_connectivity/ismrm_hcp_tutorial.html suggests (as it generates them) that that is indeed the case
    - https://www.humanconnectome.org/storage/app/media/documentation/s1200/HCP_S1200_Release_Reference_Manual.pdf does not mention structural networks

- question: importance of comparability to Finger et al.? (i.e. using an atlas similar to it.)
- further resources:
  - http://www.lead-dbs.org/?page_id=1004 (info on different atlases)
  - on the UMCD database repository: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3508475/
  - tractography in the context of the HCP https://www.humanconnectome.org/study/hcp-young-adult/project-protocol/diffusion-tractography
