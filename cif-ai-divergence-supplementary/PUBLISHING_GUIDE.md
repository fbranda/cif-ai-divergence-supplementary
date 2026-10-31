# Publish this supplementary repository to your GitHub account

The packaged files are ready to upload. **No repository has yet been created on your GitHub account by the assistant.** You must publish them using an account you control.

## Option A — website (no terminal required)

1. Visit <https://github.com/new> while signed in to GitHub.
2. Repository name: `cif-ai-divergence-supplementary`. Suggested description: `Data, code, and reproducible secondary analyses for AI divergence reveals the shape of human cognition`.
3. Choose **Public** if the editor and reviewers need direct unauthenticated access. Leave **Initialize this repository with a README** unchecked: the uploaded package already contains one.
4. Choose **Create repository**.
5. On the empty repository page choose **uploading an existing file** (or **Add file → Upload files**).
6. **Unzip** the package on your computer. Drag the **contents** of the `cif-ai-divergence-supplementary` folder (including its hidden `.github` folder if your file manager exposes it) onto the GitHub upload screen. Do not upload the ZIP as a single file: GitHub does not automatically extract it into a working repository.
7. Commit the files; verify that `README.md`, `reanalyze.py`, `data/`, `output/`, and `LICENSE` appear in the repository.
8. The final URL will be `https://github.com/YOUR_USERNAME/cif-ai-divergence-supplementary`. Replace `YOUR_USERNAME` with your actual GitHub username, then place the **real** link in the manuscript.

## Option B — GitHub CLI on Mac/Linux (maintains subdirectories and hidden workflow files)

Install Git and GitHub CLI (`gh`), then run these commands **inside the extracted repository folder**:

```bash
gh auth login
git init -b main
git add .
git commit -m "Release reproducible CIF supplementary material v1.0.0"
gh repo create cif-ai-divergence-supplementary --public --source=. --remote=origin --push
```

The CLI asks you to authenticate. **Do not enter GitHub passwords or access tokens into a chat conversation.**

## Add a persistent DOI (recommended)

- Connect public GitHub repository to Zenodo (<https://zenodo.org/account/settings/github/>).
- Create a GitHub release, tag `v1.0.0`, and publish it.
- Retrieve the DOI **from the Zenodo release record**; then update `CITATION.cff` or the manuscript Data Availability Statement only with the DOI actually assigned.

## Suggested manuscript Data Availability statement

> No new experimental data were collected for this study. The exploratory visual-model reanalysis uses public source data from Conwell et al. (2024; doi:10.1038/s41467-024-53147-y). The source workbook, model- and participant-level extracted values, Supplementary Table S1, reproducible analysis code, and summary outputs are available at **[insert confirmed GitHub repository URL]**. The secondary analysis is limited to controlled visual-model comparisons and does not represent a replication of the earlier mixed-domain extraction.

Before publication, confirm with all manuscript coauthors that the data/code package and the public repository license are approved.
