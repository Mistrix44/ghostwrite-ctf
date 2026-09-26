RULE: this file is the single source of truth. If a value changes here, change it everywhere.

Studio: Nightfall Interactive | Game: Project Eclipse | Victim dev: Alex Mercer
Campaign ID: GW-ECLIPSE-07
Build host: build-internal.nightfall.lan  (10.10.20.15)
Victim PC: 10.10.10.25
Simulated C2: 10.10.30.15:4444
Agent key (Stage 4): <we'll generate this together>
Malicious files: update.ps1, ghostwrite.tmp
Persistence: user "ghostwrite", ghost-sync.service, /opt/.../sync.sh

Flags:
  S1 GHOSTWRITE{f0rge_m1rr0r_l34k3d_7a3c91}
  S2 GHOSTWRITE{n0t_4_r34l_c4ptch4_e51f28}
  S3 GHOSTWRITE{pwsh_upd4te_dr0pp3d_tmp_b04d6e}
  S4 GHOSTWRITE{4g3nt_ch3ck1n_4cc3pt3d_8c27fa}
  S5 GHOSTWRITE{p3rs1st3nc3_v14_gh0st_sync_31e9a4}
  S6 GHOSTWRITE{c2_h0p_c0nf1rm3d_n1ghtf4ll_6d5b70}

NOTE: Report specifies Ubuntu 22.04 LTS. Actual build environment is Ubuntu 26.04 LTS.
Reason: version available at build time. No architectural impact — same Docker/systemd approach.
Update Section 7 (Technology Stack) in the final report to reflect actual OS used.
