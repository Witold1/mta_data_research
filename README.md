## 🚇 Project
**NYC MTA Turnstile Usage Dataset**

## 📖 Task description
We have a **pool of questions** and **the dataset source** to use to find answers in empirical way.

* Dataset provides data on Turnstile (i.e. tripod gates) usage in NYC MTA (Ⓜ️ subway)
  * Could be used as a proxy of subway usage and people movements over the time
* Date interval we work with is first three month of 2013, Jan 1st to March 31st
  * Some questions require different temporal slices but whole interval

Current **report available**, see [[html]](https://htmlpreview.github.io/?https://github.com/Witold1/mta_data_research/blob/master/reports/Report%20notes%20and%20processing%20code_final.html) | [[ipynb]](https://nbviewer.org/github/Witold1/mta_data_research/blob/master/notebooks/Report%20notes%20and%20processing%20code_final.ipynb)
<!--- Current **raw report available** on demand. --->

## 📊 Selected charts
<details>
  <summary>Charts - click to expand</summary>

  <table align="center">
  <thead>
    <tr>
      <th><img src="./figures/internal/VIZ4.png?raw=true" alt="VIZ4" width="300" height="250"></th>
      <th><img src="./figures/internal/VIZ3.png?raw=true" alt="VIZ3" width="300" height="250"></th>
    </tr>
    <tr>
      <th><img src="./figures/internal/DA4.png?raw=true" alt="DA4" width="300" height="200"></th>
      <th><img src="./figures/internal/DA2.png?raw=true" alt="DA2" width="300" height="150"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="2"><img src="./figures/internal/VIZ5.png?raw=true" alt="VIZ5" width="650" height="200"></td>
    </tr>
    <tr>
      <td colspan="2"><img src="./figures/internal/DA6_bars.png?raw=true" alt="DA6" width="650" height="250"></td>
    </tr>
    <tr>
      <td colspan="2"><img src="./figures/internal/DA6.png?raw=true" alt="DA6" width="650" height="350"></td>
    </tr>
  </tbody>
  </table>
</details>

## 📁 Directory Structure
```
Project structure:
+--data                       <- folder for datasets
¦  L--raw                       <- ... 1. raw data
¦  L--interim                   <- ... 2. auxiliary, generated, temporary, preprocessed data
¦  L--processed                 <- ... 3. final, ready-to-analysis data
¦  L--external                  <- ... +. additional datasets
¦  
+--notebooks                  <- folder for *.ipynb files
¦  L--*.ipynb 1                 <- ... file 1
¦
+--src                        <- folder for .py scripts
¦  L--*.py 1                    <- ... file 1
¦  L--*.py 2                    <- ... file 2
¦  L--*.py 3                    <- ... file 3
¦
+--figures                    <- folder for charts and images to reports
¦  L--external                  <- ... 1. raw data
¦  L--internal                  <- ... 2. raw data
¦
+--reports                    <- folder for reports (i.e. *.pptx, *.html, *.ipynb)
¦
+--docs                       <- folder for documentation files
¦
+--README.md                  <- the top-level README for developers using this project
¦
+--requirements.txt           <- packages to build the python environment
```
[Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/#directory-structure)
| [tsdataclinic - SubwayCrowds](https://github.com/tsdataclinic/SubwayCrowds)


## 📌 Links
> Placeholder
<!--- * Feature engineering. Preprocessing. Charts [Here](https://nbviewer.org/) --->

## 🐉 License and legals
Ask before use.
