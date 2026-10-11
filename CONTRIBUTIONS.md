# Contributions

## How this repository was built
All four members built this project together on one shared laptop (Kaldera's).
Most of the work was pushed from that one account, so older commits show a
single author even though the work was done by four people. Some members also
pushed their own scripts and test results from their own GitHub accounts
(see the commit history). This file records who was responsible for each part.

## Who did what
| Member | Area | Files / folders |
|---|---|---|
| Kaldera H.P.I.D (IT24102276) | Platform & Architecture: deployment, networks, proxy, jump host, flag validation, security controls, reset | docker-compose.yml, proxy/, jump/, README.md |
| Wickramaarachchi M.H (IT24102374) | Stages 1-3: OSINT, ClickFix web page, forensics bundle, IOC correlator, solver script | stage1/, stage2/, stage3-verify/ |
| Fernando K.N (IT24102569) | Stages 4-6: update.ps1 and ghost-diag, systemd host, persistence, Stage 6 pcap, exploit script | stage4-5/, stage6/ |
| Ranasinghe R.K.K (IT24102680) | Integration, Testing & Documentation: end-to-end flow, test cases, reset test, design changes; also helped with the stages | docs/, tests/, test results |

## Evidence
- Report Section 10 (roles and responsibilities)
- Commit history: `git log --pretty=format:"%h %an %ae %ad %s" --date=short --all`
- Own-account commits: solver, exploit and test scripts by Wickramaarachchi, Fernando and Ranasinghe
- Each member explains and demonstrates their own part in the demo video
