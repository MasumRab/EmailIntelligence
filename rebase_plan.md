# Automated Rebase Plan

## Phase 1: Critical & Infrastructure
pick 837f0b4c3be0be620537c058dd8dba25d8ac010d Merge pull request #189 from MasumRab/feature-architectural-and-security-enhancements
pick 1ac39f5a5880ffb6deb322b07598226a685b0818 Merge branch 'main' into feature-architectural-and-security-enhancements
pick e8074f024e684f8d73294c69f804f2a1b043a07d feat: Implement architectural and security enhancements
pick 0f981a043a1be8a0fbdf884dfa93a162ffda90e4 Merge pull request #185 from MasumRab/refactor-database-readability
pick cf44afd6bf1411c836f5e6c0100ca82606857e86 Refactor: Improve readability of DatabaseManager
pick 6e2362e7002756f402ebcb094c2bd1fe807d9509 Restore and enhance validation warnings in database create methods
pick f92b72e3e00690296d8eb817af0601ab789582f2 feat: Enhance core system with security, database backups, and performance improvements
pick c74b43c988e0043a5bf425cb0817b0e1e7508599 feat: Enhance core system with security, database backups, and performance improvements
pick fcc2d16f82998a3b029f26d18cb48c4301a61bbf Fix security vulnerability: Load secret keys from environment variables
pick bd027038a3a59e5bb2a9fab75fd35889a2f738fd Fix security vulnerability: Load secret keys from environment variables
pick 6a4bbeacab1072b0626652be2ca6207c52cdc0d6 Fix security vulnerability: Add input validation for host/port in subprocess calls
pick 815dcb0554afe73f6f0b416b8d9f51ca0b52e467 Fix security vulnerability: Add input validation for host/port in subprocess calls
pick e7ed34b0c4690259ce175b9da8b8d27dfa8388ec Implement proper API authentication for sensitive operations
pick 0648c733aea60a65a1b091edda56d481047ae99c Implement proper API authentication for sensitive operations
pick 6f326610730673f01ee0633b147d4e46efa37039 Update dashboard_routes.py to include DatabaseManager import for consistency with scientific branch
pick daf2bbb51475ea96f621f018e31ecb3e85e4df32 Update dashboard_routes.py to include DatabaseManager import for consistency with scientific branch
pick b90af622cb53fd05d8ab1970d6b47c4f3bed4097 Fix EmailRepository implementation: Convert to ABC with DatabaseEmailRepository
pick 9f25ab9277456b28423e680411fda4cbf70ec562 Fix EmailRepository implementation: Convert to ABC with DatabaseEmailRepository
pick 52e5b3d2f4b3c2b402ed2008c3c83d7dea3e5bd4 Implement dashboard stats endpoint, PromptEngineer class, and API authentication
pick f8d685ed5965c3445efd7b01c4679ec15523f4d5 Implement dashboard stats endpoint, PromptEngineer class, and API authentication
pick f2b9ea1b58f776b42666da26dfcd37cccf374165 Resolve merge conflicts in backend/python_backend/database.py
pick 318594cec5a88a084a1a8a4125a67a9a9cebfd8e Resolve merge conflicts in backend/python_backend/database.py
pick ed51a82962121ef68fa52c3e062027381a150b9e Complete workflow migration to unified Node Engine architecture
pick c0e4c5d5029c74ad2bd306bb46228787294147f5 Complete workflow migration to unified Node Engine architecture
pick 812511dcd91a413b561c4cb39d6a883870b6cefd Add comprehensive workflow migration plan to scientific branch
pick 68a2c7771127b5523991135b1ba127f602539c86 Add comprehensive workflow migration plan to scientific branch
pick d193a3563d884ba5d5be4cae0e78944cdf05a9e3 refactor: improve gmail api auth and error handling
pick 85401aa719d67c55bb188e279261e96ea96b3f41 refactor: improve gmail api auth and error handling
pick fdfd2965cf7b6307db3a6437f712fe8d9cb798ed chore: cherry-pick launch.py and setup files from orchestration-tools
pick 1b13767a2f9c448a91e7dc61a8fad4966b1d5494 chore: add .taskmaster directory to gitignore
pick 79084399d5bbb2c2c9072a011f7b730fd0cef860 chore: update infrastructure scripts and configuration
pick 60a1e84ce4638d863abd2ea952450fd71e103176 chore: sync infrastructure scripts from orchestration-tools
pick c76741304027b6cc06bcd8c04bbcee6d5c08df3a chore: remove Phase 2 test artifacts
pick d26b7623071edef819138e79e10b5007cb74175c chore: add orchestration tools changes and documentation
pick b2db69e0e3f2b4a15b810a3015b70dd4a7c40c9e chore: remove obsolete temp-backup directory from orchestration-tools

## Phase 2: Features
pick 22a77c07305d26de37c6f5399876168413a4883d feat: Introduce comprehensive Git analysis, rebase planning, and cherry-pick protocols, alongside new CLI, resolution, and strategy modules, and update the CLI integration plan and core application.
pick c076ba7e35855c85cfb360dc27354fb7110216f3 feat: Implement a new intelligent conflict resolution engine, commit analysis, and Git reordering capabilities with CLI integration and extensive documentation.
pick 8a97e3e74542847e8bb83bd390a9b54b10047638 feat: Introduce Git conflict detection, a constitutional engine, and documentation for scientific branch analysis and CLI integration.
pick 26b29366cd2d146fe3e84e0c4a6a5182295b558f feat: Implement core constitutional engine, analysis, resolution, and strategy modules with comprehensive unit tests.
pick e5843d7e5397de309abdc8df5f16acc32aec8305 feat: implement Phase 1-3 refactoring (core, git, storage, analysis)
pick 5b9eb60724f47f7dfe776c4ab5f1ee6c0979ebb2 feat: Initialize ConstitutionalEngine in CLI (Phase 1 start)
pick 07f228ab32b29dd6b8a1c2548ef088122d5611cf feat: implement EmailIntelligence CLI v2.0 - Add complete 1400+ line CLI tool with constitutional analysis - Implement git worktree-based conflict resolution - Add multi-level validation framework - Include spec-kit strategy development - Add comprehensive test suite
pick b4be34183582a56521abad9691e5ef872678fe8c feat: implement EmailIntelligence CLI v2.0
pick b5c1b22d2bb523063fdb19ef0924d8be788ce301 feat: add automated branch update system for script propagation
pick 1d28f84c130a364ad62ff2413ded1c15c7894f18 feat: implement branch propagation policy and enforcement hooks
pick bf1e11ffe499c74ad605e009c84a1881f94dc725 feat(orchestration): Implement Strategy 5 push aggregation and validation
pick 62c0f5d8fea6f6c198d445c6c7c8fcbbeb2ac139 feat: add comprehensive linting configuration with proper exclusions
pick e58be0e4486916332071ea817b5f833e41b2fd81 feat: add P0 CI/CD workflows (test and lint)
pick 1f006c7b5974a8634ea5c308ccb16650e194f19b feat: add orchestration workflow documentation and hook cleanup
pick 4c3c466b39423746dc0269cf221984555ff8f74d feat: add orchestration file extraction and simplified documentation
pick c30db514eadefd463461d6162f1bb424ab7a6d88 feat: add disable/enable hooks scripts for independent setup development
pick e58c1768b65b1382f3d53ddedef8dff40f870b71 feat: update .gitignore to exclude backup files and temp files
pick 30d7ad4db6e28ea415332716d5741323609fd152 feat: Add recursion prevention to post-merge hook and update messages
pick dc576617dd8acf515759dce7b19ce2b7152f1349 feat: Add recursion prevention to post-checkout hook
pick b4576fcef7ef912b35bcf002d0d1262aebb4d6da feat: Complete orchestration test infrastructure restoration
pick c1627d31d4917f305d218b23789aa4ff30e8b179 feat: Enhance orchestration workflow with key checks and hook validation
pick 22b6dbd407e4d65ba518adc5e428e5b40ba6770e feat: update pyproject.toml with comprehensive dependencies for Email Intelligence platform
pick cf21251fe43001d8dfdce5fcc7c03b7342065866 feat: update pyproject.toml with comprehensive dependencies for Email Intelligence platform
pick 02cae87e1f8f57ce2f9ba95e8e0a846d6f260866 feat: implement random SECRET_KEY generation and test environment setup for main branch
pick d3bbff6f54adaebca828fc93be278710549ae0f6 feat: Add backlog task for orchestration script refactoring
pick 2162cc1abba355f62262a18fe573878ba04f9c80 feat: Implement conditional hook installation in post-checkout and add orchestration documentation
pick 2bf182d5a835f61b5b121ab3c11e7d0ea1222b46 feat: Improve Python environment setup in launch.py\n\n- Ensure pip is upgraded before installing poetry/uv.\n- Enhance Python version compatibility error message.\n- Improve Conda environment activation and availability warnings.
pick 2610fc9d87d3919f906591892a5dce62cc5b9846 feat(tests): Add extensive test coverage for core modules
pick 344b29c41d9c0ee7cb6cad1c337d377ba0b7cd04 feat(tests): Add extensive test coverage for core modules
pick 078201c25cfca19b40170be29e4411e71a0ee47c feat: Add new backlog tasks and reorder priorities based on README review
pick cc119b26c8086fd1c3dc02ba5925f5eedfacba8c feat: Add new backlog tasks and reorder priorities based on README review
pick ee0a18ba3fa651cb62647a72e3dbcf030cc1e8ba feat(tests): Add test coverage for workflow_engine
pick 62be36aa8ad1a3abc5a886bc6dfcc5fcfca1f0a0 feat(tests): Add test coverage for workflow_engine
pick b6129dcbf85e83773564efcf931986426519d882 feat: Initialize comprehensive backlog system for main branch
pick 651f6deaa5cdcc486caf24502fda289133ecf399 feat: Initialize comprehensive backlog system for main branch
pick 69190e55ea8658f8d444e8f8a40e568964e92ee1 feat: Restore launch.py and resolve merge conflicts
pick 0e900ddf7714221bf241ebc1b0fda4fe6e3c525c feat: Restore launch.py and resolve merge conflicts
pick 88dab7cf4529c513ae0a8119e6a79f636a93c1a2 feat: Implement development session tracking and codebase analysis tools
pick bcb099c346f769a3582d3f6d59633755d1fdbdaf feat: Implement development session tracking and codebase analysis tools
pick c871f5c34a0b16c4f7c1c8f2af3d922338037cd0 feat: Implement SOLID email data source abstraction
pick 30dad352654c3f0631a63933010257ac33986de4 feat: Implement SOLID email data source abstraction

## Phase 3: Fixes
pick 17d0ac293ab3e3a627421ff1d93e1bbcbdd1c23f fix: Update conflict warning message in post-checkout hook
pick 1010afa29fab08983673aaad65f69ac661a67d5d fix: Add conflict checking for subtrees in post-checkout hook
pick a5d37ce9aa3267ea19d98258a4e017fafcb44b05 fix: Add worktree safety message to post-checkout hook
pick 55d541c70de0375eb42b6f577e1d341144ceb921 fix: Update post-checkout messages to match test expectations
pick d5c320255d00bf7caab31540dfd4faa3cf2479db fix: Configure CPU-only PyTorch and clean venv setup
pick dfdb059b5fede358d272159141bf1b9cdb290704 fix: CPU installation failure by ensuring PyTorch CPU-only packages install first
pick 36e0a376b1e7027845c6c638c1bc9fabc49841d9 fix: Configure uv to use 'venv' instead of '.venv' to fix regression
pick aff1ac4c32987330519827d3e0411b2c6b38b40d fix: Remove invalid --quiet flags from git checkout commands
pick 8a3894ff4463ebe8a181a22ec7d6b0d87af7de3c fix: Reorder post-checkout sync to sync lib before install-hooks.sh
pick b98800f1d11611aed4cd80b731283807b2bdfec9 fix: Sync install-hooks.sh and lib to enable hook installation on other branches
pick 7daf8770d1db5c34cc577b55d215d0fffdfc9f64 fix: Correct post-push hook syntax and update hook validation
pick 100a737b9603be75938e0f3a873b337074ef3187 fix: resolve remaining merge conflicts in backend files
pick 8bb8adbc748260da12737f6280dfb82ccffd6e89 fix: resolve remaining merge conflicts in backend files
pick 55d0cef6767623de5d52572d9f0891f279d61a48 fix: resolve merge conflicts and syntax errors in gmail_service.py
pick 72150ac64d2f8bb7f50666a7d4ae575171e1c841 fix: resolve merge conflicts and syntax errors in gmail_service.py
pick cef58772e7b9df894e7c8e9f95f9e4da10585f14 fix: regenerate uv.lock to resolve merge conflicts
pick 7006035e02d0917b19cd39e0542bb9c7ee7fc1a6 fix: regenerate uv.lock to resolve merge conflicts
pick 0c835cf63517fdc130cdd36b9fd1ff05e01bce85 fix: complete NotmuchDataSource implementation
pick 4b1c1cd905dcf28250466bb9ad30afdef292f80d fix: complete NotmuchDataSource implementation
pick 4eb7e634769a05aef7082b0c2339bcf4b9ed41b8 fix: update .venv to venv in scientific branch
pick 466c1d7152de42ea0dc1502151936e10645eb2e0 fix: update .venv to venv in scientific branch
pick 613fa9e2c79f54a26b95658965e4beee9173c3c5 fix: update .venv to venv in fix/launch-bat-issues
pick bbf9198e741ae86f2f7e5cbde974c8aa9305265c fix: update .venv to venv in fix/launch-bat-issues
pick 14771dc76f5cf0f50ecb5585aa45808fe1f74d37 fix: update .venv to venv in fix/launch-bat-issues
pick 24af9ea8ea719e5fa9340c7b3ce0f703ab14d4bb fix: update .venv to venv in fix/launch-bat-issues
pick faacfbaf9fc81e21d266104f1e68bfcd072f9e9f fix: update .venv to venv in fix/launch-bat-issues
pick 45732e0e0eb15a8f8e5545abc9af9ef4564a6846 fix: update .venv to venv in fix/launch-bat-issues
pick a6c8ff53b443d65ff52bb274a4a37d654b25087b fix: update .venv to venv in fix/launch-bat-issues and ignore sensitive files
pick 15cf72471c0d678ea79aa87f83675c1f6dc3c14d fix: update .venv to venv in fix/launch-bat-issues and ignore sensitive files
pick 0e0a1c35d314bcafd764bcc0204af228e0741596 fix: update .venv to venv in fix/initial-attempt-and-reset and remove sensitive file
pick 7531c73ca4ec04615cbd1ee6519416116337fc88 fix: update .venv to venv in fix/initial-attempt-and-reset and remove sensitive file

## Phase 4: Documentation & Cleanup
pick 89d0ba83fcab9536f4dd822399b801a420876cf3 docs: add comprehensive documentation and task-master guide
pick 85c264ece19bbfafb8a4e31da1c234d05e6884e3 docs: Add per-branch orchestration hooks control documentation
pick e37418302e49eeb45a9a0d0a0d59e70a7e52f893 docs: add quick start guide for branch update procedure
pick 4f221f108959487b63150f596f6ef0ea0022e037 docs: add comprehensive branch propagation implementation summary
pick 6c17b72cc3b064d4f7b385d408c4d16ef6f4af95 docs(MODEL_CONTEXT_STRATEGY): add comprehensive model context distribution guide
pick bc676d274f9876ff1b2174028c722ba5bbe1cd1b docs: create standardized model-specific context guidelines
pick 2b3081655ae0a489a3e1e6f0b2408ce8678d9f9c docs(IMPROVED_PROMPT_ANSWERS): add Strategy 5 comprehensive answer (92% quality)
pick b920f80f843838100e04031d45128e1dd890b9dd docs(AGENTS.md): remove specific tool list from non-Jules section
pick 75bedfd41611c8c3fe86a5c425cc2f8ec8f8b05a docs(AGENTS.md): update Jules guidance to encourage learning and adaptation
pick aa3db8b44714eab2ae567c3c3cc994ad2ceae958 docs(AGENTS.md): correct Jules attribution to Google (not Sourcegraph)
pick de0c5f5a565aaa20ad924d272337f9a404118c26 docs(AGENTS.md): expand caveat to include branch-specific guidance
pick 41a5e7858341539e16a9a44acf333220ba0b05bd docs(AGENTS.md): add caveat for non-Jules environments only
pick 6b5a0362bc28c759f2f95ade0ff3b4358d013a70 docs: add comprehensive orchestration process & strategy switching guide
pick dc3e9b8231b554028573c28b6b02eb597b14c699 docs: add Phase 3 rollback options and orchestration workflow
pick e350e09adc66d71502b38112ea4d1a49efe3a64e docs: add comprehensive tools manifest and context loading guidance
pick c6d5f8811b9a9eebf2499faa8f02936fc159df37 docs: add LLM documentation discovery and processing flow guide
pick ed2c12e342d8bb73f1f58ededca2bdf3516249f1 docs: add machine-readable orchestration specification and agent checklist
pick 1e512d3133769a0a4bc51a81bd083b003bd1ebf3 docs: add comprehensive review of orchestration branch documentation and scripts
pick 35a0ca50e7eb8dc64864416cd599b79947901693 docs: update outstanding todos and agent documentation
pick c545f0c204f72f46b55c4eb015051300f3665cee docs: add comprehensive orchestration workflows and implementation roadmap
pick d4f60e00d1e948ac8e7d46325c0c08d84015d534 docs: add sync framework review and updated single-branch options
pick a5107c12ee65c192102442cdceff376a0dee4d5a docs: add simplified orchestration guide
pick 2dfdbd72849a7cd19ce7703e839f757ef023b550 docs: add orchestration quick reference guide
pick c8c65390f43e836283ad64c7920abc61accc9b8f docs: add comprehensive orchestration push workflow documentation and PR template
pick a2775d6fc1d0bdad706c3650edf87ee0c1ae4e83 docs: clarify setup_env* file sync in post-checkout and post-merge hooks
pick 9fdf271cd74766ffdb735e1ff731efa2b8464d72 docs: update test migration assessment - scientific branch has superior tests
pick 3787b367250eb976de9f09fd1bfafcbb68cd0c93 docs: Add comprehensive hook management guide and update orchestration documentation
pick fa7beb918f8fcf1386ed30215634fc6ebb5641cd docs: Enhance orchestration validation tests with clearer instructions and troubleshooting
pick 57ea5d29d112fa14d3ec4f7e9aa231b553157796 docs: Organize and improve documentation clarity
pick cea65f563ceb35cd19578855defc91ea3805d78b docs(merge): complete Task 73 - Update Alignment Strategy for scientific branch
pick 0a00d987cd0ca2212ae73659d1ce271744148638 docs(tasks): update task 72 status to completed
pick 9e593eec24c06f6a831080b05350a650819f5ec3 docs: Establish CPU-only deployment policy
pick ce333dde13bd379cf92201d0e81ea3bcc2f67a1e docs: Establish CPU-only deployment policy
pick a726d30a0a65fce54dde3b1e8c6bc0a00eb59044 docs: Add comprehensive NVIDIA GPU dependency analysis plan
pick d0faf04295487887ec8a32dc09c89ad2c3ac6781 docs: Add comprehensive NVIDIA GPU dependency analysis plan
pick ba52199686b56e1b58f26e8d1f5982443e21547f docs: Add unified architectural plan and comprehensive backlog tasks
pick 0a2a654200f9cc7e9324f8df324673181280767d docs: Add unified architectural plan and comprehensive backlog tasks
pick 15a3723909809f62a44092c060286a51ee5cba3c docs: Add analysis of duplicate files to refactoring plan
pick daaaa6e9aadaebfaae0366424b1b1e49faadbbfc docs: Add analysis of duplicate files to refactoring plan
pick 0c0cfe6dd0bc76f1de492670e7e22bc71022d1fe Merge branch 'feat-emailintelligence-cli-v2.0' of github.com:MasumRab/EmailIntelligence into feat-emailintelligence-cli-v2.0
pick 8e930f2b26f612e891ed4cf63683ac5ec0d32f36 Merge branch 'feat/emailintelligence-cli-v2.0-with-pr-framework' into feat-emailintelligence-cli-v2.0
pick 830ce29e183098f2db68d96ce517bd6e56b781c9 Merge branch 'feat-emailintelligence-cli-v2.0' of https://github.com/MasumRab/EmailIntelligence into feat/emailintelligence-cli-v2.0-with-pr-framework
pick 77be6d28513cd34e97789df2bc784fcb4e350cd8 partial progres
pick 4c59f86826ed4e33f660b43c13a62c1222adb380 partial progress
pick 5350eab014f22e28d8387ace5af243a8208910f7 cli updates
pick 2e3c5f8a0876921cc6fe7192e91ef7130f265c7e Merge remote-tracking branch 'origin/feat-emailintelligence-cli-v2.0' into feat-emailintelligence-cli-v2.0
pick ac714fa25c083ab06b1e82b6fc84085e164933f8 Fix import errors and install structlog
pick 306757176dd247d846c25dc69add5eceee15b56c Phase 0: Fix broken imports and create comprehensive analysis
pick e29a4d1076d79096aa55caa1b91d39915360c551 Merge pull request #207 from MasumRab/feat/emailintelligence-cli-v2.0-with-pr-framework
pick 6eb7c26308623b96fb2858b3d16cee787315c331 Fix SonarCloud code quality issues: format code with black, remove unused imports, fix spacing and newlines
pick 9da426bb92b683ec9fa82bb0edf87db980be8d61 merge: orchestration-tools-changes-emailintelligence-cli into feat-emailintelligence-cli-v2.0
pick 81b31d2074724065bdfe40f3e342f5669c42e85c attributes
pick 6722bf1b42c28e6f44fcade4d1b81245eafe0af0 Update orchestration-tools hooks to support enable/disable on non-orchestration-tools branches
pick 982bfbc5487913eb929ea7f9a7db447a4eb3c4d9 docs
pick b77b40f6c4eb9fc18107e76de93a850b700a85e8 merge: orchestration-tools-changes → orchestration-tools
pick e1ed9a8ef43b7f544036380a76af0eb8f9a74a43 test: add LLM single-shot test suite for orchestration documentation
pick 921b9ea7ea2a0c902a229087a0811383db026fa1 Merge pull request: Strategy 5 push aggregation with Phase 2 validation
pick 9636ca806721d1c6e9009910ae1d5cf408ee30c3 test: aggregated commit 3
pick 53872fb69f9c1572f4c8cdf562aa213b4084b810 test: aggregated commit 2
pick 0b73f550e4ae08bc358a86004e50182facf55153 test: aggregated commit 1
pick 7b223ba5ae320ac09d771a9d50482e82fc15d1b3 test: multi-push simulation - push 2
pick 9b55ec4590d3adf7c0a4c84f028234e4d6336783 test: multi-push simulation - push 1
pick 8293c1319c0e1d991eabe87a15bc507bf7a76498 test: Simulate agent push to orchestration-tools-changes
pick 2abe41e3353a7791fb433c937644cc0ec7385b83 Revert "Merge main into orchestration-tools - complete merge with all files"
pick 602615fec61f52c0382abc0312e8fcf2a920f73f restore: reinstall git hooks for orchestration-tools branch
pick f63324d997c5f260c8671aaefbee2438263266b2 Merge pull request #201 from MasumRab/orchestration-tools-changes
pick acdbd43408ed1c8d06cffb9054fc63b26387a567 Merge branch 'orchestration-tools' of https://github.com/MasumRab/EmailIntelligence into orchestration-tools
pick 65f3465d39377436664dba92d676e5f3981eb09c Merge branch 'orchestration-tools' of https://github.com/MasumRab/EmailIntelligence into orchestration-tools
pick af4d6b4d1e02ae09365895b926ae22ce199f2b08 Merge branch 'orchestration-tools' of https://github.com/MasumRab/EmailIntelligence into orchestration-tools
pick eaa87be62ec96ca010f5393f7a106e794549bb1b Merge remote changes from origin/orchestration-tools
pick 19432490e83ae3d692c14d87e58200d5306c9b8d Update managed files: pyproject.toml, test_hook_recursion.py, and uv.lock
pick 16255c79f81622c307e55ac1290fcd9ba2cbd2bc test: Add comprehensive Git hook recursion prevention tests
pick 55a89f3a963e281cac2b0028e3cd0ecf520ba5cf Merge remote orchestration-tools branch
pick b5fce728bc7f41bbe4e00870f8a1a39f6b470554 Update orchestration-workflow.md with current core files list
pick 4cb20996715f2d9012146530155adc700565b3c8 Remove low-scoring files from orchestration-tools branch
pick 421317c7c23aaf01f2b4cbf1ef4dc1aa3e87269b Merge main into orchestration-tools - complete merge with all files
pick a6c87eeee930f6c3de33c7e92c9e67af44704055 Configure uv venv path to 'venv'
pick 00eacbe0b0f0dbcddaf4ebf001622ad4dc9e2526 refactor: Move orchestration-workflow.md to docs root and update managed docs
pick 91bfc0d32bdb4ccd940a53e73938e2fe0312fa9c arch
pick c082a4388947c5c6cd6be4cabbf63048217abbd3 Add remaining orchestration and setup documentation files
pick 8293f9647d5c59fa5a3d46d023c90f960eb6904c Merge pull request #194 from MasumRab/remove-deprecated-markers
pick 8e3c5b0d5f6e4a4535e1a09c14e0b72de9e2b6ea Clean orchestration-tools branch to contain only setup and orchestration files
pick 87dfb1c925f3528988cbc89a420cee3ab0cbbf65 Fix CI test failures: Resolve dependency installation issues
pick 02c7730ba33c3eb92b364c589ae2b138efc0affb Fix launch.py for PR #194 branch - remove command pattern dependencies
pick 1b06346939b548b9cbd4cde42ed01f078d92d118 Merge branch 'main' of https://github.com/MasumRab/EmailIntelligence into remove-deprecated-markers
pick 74b486f5e55a6a87816edec39d72fce7efc662cf Address Sourcery AI review comments: improve email address extraction in gmail_metadata.py
pick aafd4a29d8ff8682c12e014e5de143d394c4147d Remove DEPRECATED markers from backend modules
pick 3e71949f5d2f116854e7f8ccbf225177a6416976 Update agent configuration and documentation files
pick 550e434b704a78830fc421d6dbf33b91dc005dad Test: uncommitted change for orchestration sync test
pick efbd41d666ae18025d530b739287d0e9bc195525 Add critical files check functionality for orchestration-tools branch
pick d6ad8dc07b7d270075f264009488983b5eff3cf3 Clean up orchestration-tools branch: Remove application-specific files and add clear documentation
pick c33f40fc03b4c9b03d705f2e398798bf32ecdcf9 Remove GPU dependencies: Use CPU-only PyTorch versions
pick 53fe32b6131b6a9741189af36e1f933f025fe338 Simplify: Remove complex environment-specific requirements files
pick ead5b80f92174fd5f536e44f834fd60fefb8d0a6 Fix: Correct git checkout syntax in post-checkout hook
pick 044dc1bd3f55c25516d40578a3b05a64cdceaa4d Centralize Python environment files with environment-aware orchestration
pick 1c5f79b558c640c19a862bf0bb92bd144877c1d0 Test: Modify orchestration file again to verify warnings
pick d51ac23bdd2b41e77cd108bcea00634013f128a8 Test: Modify project file to verify no warnings
pick 772bdd418a735b9c2a51c68f75e51638c915fa6c Test: Modify orchestration file to check warnings
pick 747cffa1c8fd917e44243d161cdbd989ec232ad7 Clean: Remove orchestration-managed files from main branch
pick c7a104304205d0ba88d2b47cb9b42e338a98c869 Test final warnings: only orchestration files should warn
pick 3fb10bebf671b83f0a4638175dea98663e0085f4 Test selective warnings: orchestration vs project files
pick 75c6ca300710e727c34ad2b53c4cb4a8843db277 Fix pre-commit hook to only warn about orchestration-managed files
pick 237c5e1785bfbcd772b20440ea236f0d8c34b27b Test pre-commit warnings for orchestration vs project files
pick 157e977af1a495231c4ee13e6c1fda281ebdf6cd Fix post-push hook to only monitor orchestration-managed files
pick 7a26507929b12afb2397543359ed28f29e57c981 Fix syntax error in post-push hook
pick 0b4b8a1ebc78224d69eeb2c1b62f927a954f57c2 Add comprehensive documentation for hook version mismatch issue
pick 0da1432ae9b0d99106c2d2dcecfa137989ed782b Fix install-hooks.sh logging and error handling
pick bf791d6d6d03859e41fc6edc4269882561513008 Fix install-hooks.sh to pull from remote orchestration-tools branch
pick 81d9489b82a3bccbc4c6a4154d42b279c4b52975 Update orchestration documentation with comprehensive workflow diagrams
pick bfe103c93bf9fd81776089bf98e00480bb7e2012 Add shared utility libraries for refactored hooks
pick 5c39efcf56c29c712318d953ec6faf02b40763a8 Fix: Remove orchestration files from main branch
pick d52a8110986dddd8a237a83f78a7537f5d935012 Fix linting issues in launch.py: remove unused imports, fix bare except, format with Black
pick f9399365784615dda6982fc617c0a99eab788863 Reapply install-hooks self-update and file restoration changes
pick cba3dca5b65f3727d465053a4205e5e80f095061 Restore requirements and config files for launch.py
pick 552366a075e9a22cb7ac76d4048beb255d17a532 Add cleanup_orchestration.sh to post-checkout sync
pick 0ba19c0b05f01d8290eccf2fefb0bdc14021b180 Restore full post-checkout hook with orchestration sync
pick b8a4fd2fd6853d627d0b67cb3d632ac4215433ad Add self-update check to install-hooks.sh for user choice
pick 2f0a242eb474b2f6bc3b789cfab4d7dfba1c528b Add cleanup.sh script
pick 9600ee18a08dd8bc0017a4b8015b016ad3919e1e Simplify cleanup to only remove orchestration hooks
pick 135c86108ba656375ca0f5f3a52eebf8f9d277d7 Expand cleanup to remove all orchestration hooks and scripts for consistency
pick e36307948e25afb0f4ca1a5b2abcc02cbf0ba556 Add deployment directory sync to post-checkout hook for launch imports
pick 2f38d60c893fa4ee120346451a0d9a6f68bfc0a0 Add deployment directory with test_stages for launch imports
pick 0829195fa0bb2f82073fc19dd91991e947c3b21e Remove exceptions for main branch from post-checkout and post-push hooks
pick e300f46ed46b30bcf941b882561c088841430f65 Modify install-hooks to pull latest hooks from orchestration-tools branch
pick bb254fa6a46bbdb1d17dc2d8af71e832a87ff202 Remove extra orchestration scripts from main, keep only install-hooks and cleanup
pick 3ec87e4e2b05971c253b3cd8570600c3619bd197 Add user confirmation prompts to orchestration cleanup and post-commit hook
pick 82d4d14f02d1b9959a9ada8078af4b07ec34c77b Remove frontend config files from orchestration-tools branch to maintain clean state
pick 8f746fb609d4aeb7e72223f96817d6aabb2118d5 Restore missing orchestration-managed files from main branch
pick 58c57ac325eb4ed37e44bcfc12b4440a72a2975c Add orchestration cleanup script and regenerate uv.lock
pick 6e8c5ebf82428022f21bee285025a804fc906297 Restore and enhance orchestration sync in post-checkout: improved messages, corrected warnings to info for missing files
pick d572a009d81fa975f685bbeff6dbe8256dadfdfd Remove project-management docs from docs/
pick 43951eaa5a6b86cbadd62d16b0b55a640c52b586 Fix warnings: Move intended scripts back to scripts/, update installed hooks to use cleanup
pick fa600e8ec1dca271a3a453f34f6ef96776ab122b Restore intended launch.py and setup/ files
pick 9804d9d978996bc6ae4ea1d4a9a14b4db4c47b2a Add branch_switching and workflow guides
pick 4545616b27bcb4188a165d8edbe65b1a7a3cf160 Add back launcher, deployment, env_management, and branch_cleanup docs
pick a8c886f759df23f072d3f96951b0126d5c10c0cb Minimize docs to orchestration and syncing management only
pick 0ac21a88bf444f1eef747208bfa76f2c5753e905 Trim docs/ to critical documentation only
pick da8c3d3473ed68cfed177b383c2be423683f7aea Restore comprehensive documentation and orchestration tooling configs
pick 2ebb945219c961bed9b3418788832f31e174c77b Clean orchestration-tools branch to only include scripts and src directories
pick 585ed9b14a2a902a223666af4465642d582e5340 Fix install-hooks.sh grep pattern
pick bd9679719228bb39aa0b902671189a3d8e09cc05 Restore reverse_sync_orchestration.sh script
pick f95117966403f21eedc7bd728cdad83137551a7f Create install-hooks.sh script
pick 875402f02c38da886663477d0db0aaf738814edb Add launch system architecture files to sync script
pick 14bef1b1ba4813bcd73621d4623d0918fb25e26b Restore SOLID Command Pattern architecture files
pick e45e625444fd4e2b7ef095b3c19914486f7abd96 Update post-checkout to install hooks after syncing canonical files
pick bcd614b4e2b5c70a1b0276c38ce80a01786cd49c Update post-checkout to sync canonical orchestration files on branch switch
pick c92313766746e0d6f0c36a597d045cde60d19b19 Update pre-commit hook to allow orchestration changes with PR warnings
pick 802c8bca741dd6d6057318102fdb5e74433a6305 Modify hooks to allow orchestration changes with PR requirement
pick 1f0fc1551c03e062dcc7c73a8c0f6a4fdbd2d09b Add root-level shared config and launch scripts
pick 51c8857f79b4cbbe56f812daf7748b11776ee07b Add orchestration setup and config files only
pick 3df9f6fe051cd1518f90230295df439303091aad Add orchestration files to main branch
pick 1feec9e391d26e9094658e0847c332125b632737 Resolve conflicts by keeping updated versions
pick 8d40afda306c7aef7556e19f7ee8260805ea042c Complete Local Development Setup task and resolve merge conflicts
pick 0e24a93d19c106338b213a06c6d686755433faea Update docs/server_development.md: correct directory paths and run commands to match current project structure
pick aa2263ccb8b2aba8f25d5bfa01950c49798c00b5 Fix invalid paths in setup/launch.py: update TypeScript server path from 'server/' to 'backend/server-ts/' for consistency
pick b81cc35c7b159b4aefdd1aae88342a7db778eabc Remove outdated task-73 file after consolidation
pick 2f62244fb624a3f984771f36ca150bb681e6c720 Add documentation sync script and update gitignore for worktrees
pick 26fdb1fb539e0ae47d1308d16c4b8cbb6b6268a8 Implement worktree-based setup integration
pick 4f8a22510d157c3b4d7e627217f96039858f4846 Integrate scientific branch features and enhancements
pick a582237c3f61a17cf6e98fc74531344eadbcd3f6 Fix notmuch dependency version to >=0.29 for compatibility
pick 0907b636a04f3f8093ce604972e7f1702781e9ae Add hook installer for automatic environment setup on branch checkout
pick 0cd14252f272b4e7f834efc754a6bce53bb8dd3d Fix subtree setup paths and imports for correct ROOT_DIR and dependency resolution
pick 70ffcbead43313d4abe95aab75eff6ae9e35bed9 Add untracked task file
pick 16488275c3defc521599e947cf961642cce09ade Add tasks for remaining Phase 3 PRs: 3.6, 3.7, 3.8
pick c83c2da6f96ee7945489bf4afbac113cb0f28280 Add task for Phase 3.4 automated alerting PR
pick 18054d7b217b9b718d0c2078694b2d216b832ce0 Add task for Phase 3.3 advanced visualizations PR
pick 741d48cbe19524bb67aba89a1ef5486b460c8f58 Add task for Phase 3.1 AI insights engine PR and archive documentation
pick 0de937b97b61916c949a7f39b1460ed0d3a59ac5 Add completion report for launch/setup branch deletion
pick 06ce95b885e98c42372135c6fc402f3b2444c680 Add missing setup files: .env.example and README.md from launch-setup-fixes branch
pick f9665c53921cd9911ec5bd62bf2f5f5eec80172b Fix setup directory: create proper setup directory with only essential launch and setup files, replace overly complex subtree
pick 69a27f2bdb9a5f60d67d4f8ca045947dfbc88ccb Clean up nested setup directory files
pick b64da4a29fcb516af412070b7f39760406fed983 Add wrapper scripts and symlinks for backward compatibility with subtree structure
pick e4875d800d5aeacc92bd83478e59bc25bb26ab9c Implement subtree integration: moved launch and setup files to setup/ subtree directory
pick f4f9037975ebf6ebcca081bdd39266fab4ed8fd6 Merge commit '93a3140d8efab2d854e6ba3fd8d2989d1ba918ff' as 'setup'
pick 93a3140d8efab2d854e6ba3fd8d2989d1ba918ff Squashed 'setup/' content from commit cd39f02
pick b77a5525eb8788bf07eac704ff9b5aa4feefd883 Complete main branch subtree integration documentation and update task files
pick aeedd4d5b68307f0e446a25a66963177806888bf Prepare for subtree integration by staging changes
pick 9e40f10bc9e0ae970525e0a5adebe6ca6dac23b7 Merge branch 'main' of https://github.com/MasumRab/EmailIntelligence
pick 328c47fd1d19d4f18f79abbc2bd4e7c9123aa353 Resolve merge conflicts by accepting local main branch changes
pick 85c216c252d6a1797e2acb0df4303e7e448783eb Add models/*.pkl to .gitignore to ignore test model files
pick 6434d2f3041a04fb03910ffe0562dc5bdc2ca58d Update rebase task status to in progress
pick 0e85e39ae6da70cce9b2e15db9264eb2037e1011 Update rebase task status to in progress
pick 6899b6778f63c7d669fc86dcfd7a69b6327deaa2 Merge branch 'minimal-work-reordered'
pick 66cf02e83d5b44407d898704850f31cfc6fad45a Merge branch 'minimal-work-reordered'
pick bef123406aed92fae1df1af60b208ad8876cb438 Fix venv creation: update setup scripts to use 'venv' instead of 'emailintelligence_env'
pick 91a65db02f875b2fcc50ce8f1f6193cea9d33727 Fix venv creation: update setup scripts to use 'venv' instead of 'emailintelligence_env'
pick 07fbf0558d631bb4a2afc2e2e52e2c062e689970 Remove remaining duplicate sentencepiece verifications
pick 710003a8071d4f6d52244de715e1e11ecbaf82b1 Remove remaining duplicate sentencepiece verifications
pick 0a47d75a584b3956f78ff0bde3d61adfb687f11c Remove duplicate verification blocks from installation flow
pick 57a0b9b4fc0e2f38f8fd5fec275b81092d847a2d Remove duplicate verification blocks from installation flow
pick 8aa052fa4335cce79fc230f3721d47c71c6a6491 Centralize all package verification to the end of installation
pick 24ba84a895df09ae401336af4dfa8f4a59071c0d Centralize all package verification to the end of installation
pick bf73ab9b5ccecc285ee971adc2ff698341cea53c Fix all remaining __version__ attribute access issues
pick 3935a1c6ec12a0f676c7c319a4f891082b6762a6 Fix all remaining __version__ attribute access issues
pick ff98ab52320e8a6e5e6be674eb5b25ad1a5707e9 Add --quiet flag to pip installations for cleaner output
pick d8556889dd06445c9e91ba421d0e8d1ea3138235 Add --quiet flag to pip installations for cleaner output
pick da70a10e79f65ca3e0e47d97d0875aaacc2f34ad Fix version attribute access for packages without __version__
pick 17350978dc70cb654a2d92aa4f4829a875ed7bb5 Fix version attribute access for packages without __version__
pick 42fe2c38c317ec4bedf441cc1ac3f76940abd209 Add timeouts and progress indicators for large package installations
pick 7dc78937abb63535b2918f4de6b664a59c0ddfd4 Add timeouts and progress indicators for large package installations
pick 08a1a15474685283ff2b2278703325808a900913 Add optimized setup scripts from scientific branch
pick e22b03f099ca5a0dbfa776b19e220228a0366e0c Add optimized setup scripts from scientific branch
pick ffde63d93e46647917e22cb918945dc5aef0d90d .
pick 0a460f699b521983122adb930f80c43e40801a3f .
pick 47ac4a29f6e328f3966e802bbf7b4b078851ae1d .
pick 98061e9b03db4ee0b65f6d7963c8416c84f7b6a2 .
pick fa51d9ccbd7ea3d3730b1cea1616aed2d3b7416b .
pick d8cbeff54dd5191f628d0b6fed70fbf88759d1f9 .
pick 22b92d12e27d4dc5dc1f3a188442f6140197b82c Merge branch 'main' of https://github.com/MasumRab/EmailIntelligence
pick 72622b942d6996772dfd16a32f9c6f410e824cc7 Merge branch 'main' of https://github.com/MasumRab/EmailIntelligence
pick 2c067d14bc000c1169d293a40f99c713e942f89e Merge branch 'main' of github.com:MasumRab/EmailIntelligence
pick d8fc1f1e2aaa683a8a429ab3c0fbb3b875ce6276 Merge branch 'main' of github.com:MasumRab/EmailIntelligence
pick dce26f4a27c99903be706a797deca999243f885b Merge remote-tracking branch 'origin/main'
pick 185f7aff6c9692d3deb935bc22275bda8403eb79 Merge remote-tracking branch 'origin/main'
pick d2a4c4320d3e9b28ae25ccda12d62945fe54b7bc Mark SOLID Email Data Source Abstraction tasks as completed on main branch
pick 47086e9bb3d9dc59940bddf29cb230b8a21895e1 Mark SOLID Email Data Source Abstraction tasks as completed on main branch
pick d8031247274c8737a019087553be70e0b3acdfad Fix syntax errors in training_routes.py, nlp_engine.py, and smart_retrieval.py
pick 2b2eaf57ed5c83fe557213bda510ac4208ce576f Fix syntax errors in training_routes.py, nlp_engine.py, and smart_retrieval.py
pick 4aeae2e5dc074f999d064c4a34f70c81494165d1 Merge pull request #156 from MasumRab/test-coverage-improvement
pick 758622015856fb41465d664afee22e9378cfa9e0 Merge pull request #156 from MasumRab/test-coverage-improvement
pick 5c749e9888fd1be3a759f76ba75e4e0c74c40aea Implement PR #155: Environment Optimization and Platform Enhancements
pick f72f72c8bc23e4b0d20e4f727df6c3f34c808b39 Implement PR #155: Environment Optimization and Platform Enhancements
pick 0c16140b62b3238a7c257b0829d86daed683140b Resolve merge conflict in task-17 and update status to Completed
pick 636f502be1e2af6f646859ff4253fcc5a4410b9d Resolve merge conflict in task-17 and update status to Completed
pick d578c5f118ad25c8352361ddbcc222f640ef89bb Complete workflow engine enhancement task and update related backlog tasks
pick 503754f85f114db3471004661bd8176d6554ef15 Complete workflow engine enhancement task and update related backlog tasks
pick 12b3465b912a0165455950f2ee3ed9c8be7b59b4 Merge remote changes and resolve conflicts
pick 3ada49d19f051c2c8072ad6bb3b625a2ef4a9830 Merge remote changes and resolve conflicts
pick 0f834a3bae074a066acebc0b9df29e33c1266abc Merge PR #144: Implement SOLID email data source abstraction
pick ba4e736af30b566401bbb6c2f022c90ea4360851 Merge PR #144: Implement SOLID email data source abstraction
pick a06d5f0578aff6e67b6c7e513f72fdabee7ba910 Update task status
pick 7712667b8ee645c1d49b3871ff4187e363674c20 Update task status
pick 264732656321e608ade42e9184a3dfdb11398d20 Implement EmailRepository interface and refactor email routes to use abstraction
pick 88c9d14adb4725d0cb7e6d789efe4de9756aed50 Implement EmailRepository interface and refactor email routes to use abstraction
pick 6adc5976555d31636b592479e6041da29c1e5dc9 Add backlog tasks for EmailRepository and NotmuchDataSource on main branch
pick 283eb499a61e72fa421542511e4a44ca84681c71 Add backlog tasks for EmailRepository and NotmuchDataSource on main branch
pick bad7e092402944b27d6fc7135df533fbee562b8e Merge branch 'main' of https://github.com/MasumRab/EmailIntelligence
pick bc54f5c8c8604aa8af3e9d3cc43af4c0b1a2d788 Merge branch 'main' of https://github.com/MasumRab/EmailIntelligence
pick 02b0542b61df5e27cc49a9e234ccffced74e22f1 Fix import issues: Create new performance monitor in src/core and update deprecated backend imports
pick 76dab7bc1ab56b02e5d5950ddbdcf53e45a5c6e6 Fix import issues: Create new performance monitor in src/core and update deprecated backend imports
pick 86cdc8b2ac608ec5d1b71f769f8ebe782ae46366 Consolidate duplicate IFLOW documentation files into single IFLOW.md with both project and iFlow CLI information
pick f716c41186e40e48ab443ab6502d9fbf4a7e2f2a Consolidate duplicate IFLOW documentation files into single IFLOW.md with both project and iFlow CLI information
pick 8469b073d752fa3ed03e93430da4c906236feb3c Add documentation for enhanced filtering system and update README
pick f11b20eed8d7958e6b6b3c907117244c769c9bda Add documentation for enhanced filtering system and update README
pick a789fb764bb05875e26b1cd212e920a93b3f0f96 Fix code formatting for enhanced filtering system
pick ab7fe65944a33c7596ba8e2d8526607a6d60d654 Fix code formatting for enhanced filtering system
pick efb192f8119a85c6eb18922195e2d1afa198faf8 Merge remote-tracking branch 'origin/main'
pick 903ea2c0b08bb3412dab37b0f945b490b1e41ff1 Merge remote-tracking branch 'origin/main'
pick c7fd2aa54eff7579ac177c0f5ffdac01f752e205 Enhance email filtering system with advanced criteria and UI
pick 1ed08bfe316fd1c96d99c789ed69d06ebacd3e62 Enhance email filtering system with advanced criteria and UI
pick bc5afd26709c21362561fbbe19c3a069bc6b569f amp code cleanup
pick a30ab6bb999f6942ea7bbe76453a29b5c58704ca amp code cleanup
pick a5157aaf5232615007878c9c6c3fba05617db6b7 Restructure backlog tasks: Defer Docker-related tasks and add simplified alternatives. Create deferred directory for low-priority Docker/container tasks. Add new enhancement tasks for AI analysis and workflow engine.
pick 932d9037407f4bb75086f684dbc4e2d36f6e652f Restructure backlog tasks: Defer Docker-related tasks and add simplified alternatives. Create deferred directory for low-priority Docker/container tasks. Add new enhancement tasks for AI analysis and workflow engine.
pick 634906fdd6a9d4bd3faf915a7c5ddeb340e569b6 Merge pull request #152 from MasumRab/test-coverage-improvement
pick 0469228288b2fc9b8084ed6772e3f096a50c7aa0 Merge pull request #152 from MasumRab/test-coverage-improvement
pick 58c4cfb7b7420728d0a40c8c7b1321a4325fb808 Standardize virtual environment directory from .venv to venv
pick de12b6762073187d30212e16dfb917553262085d Standardize virtual environment directory from .venv to venv
pick a9ae318e7f6f37a55e01aab4c092fbfdc643d727 Merge scientific branch into main
pick 1e7f5d71ce835b1dafe7c1cacb30a65509a642eb Merge scientific branch into main
pick 5b2428f4c104b6cadb75931fbdf711adb4263f9d Merge branch 'scientific' of https://github.com/MasumRab/EmailIntelligence into scientific
pick d5a7a8b397aec3715bef1066922aa98e53db6b45 Merge branch 'scientific' of https://github.com/MasumRab/EmailIntelligence into scientific
pick 27380d36555cd48a97f62d41b4d7e38d35ff29f5 Standardize system diagnostics across branches
pick 3e2ddd51e3a94d93b850a638b37053d33c350ef0 Standardize system diagnostics across branches
pick 8992c605781b15349b2a000303503ee2d30026bd Fix syntax errors and missing function calls in launch.py
pick f825a868b2539d8d915b504b9dd9f1b26d082c95 Fix syntax errors and missing function calls in launch.py
pick 454119766c5164ee1e89bdb6584c43dfbf5dfac2 Merge branch 'scientific' of https://github.com/MasumRab/EmailIntelligence into scientific
pick 895fdc882ccd67686800e5921d334c5caac3c19b Merge branch 'scientific' of https://github.com/MasumRab/EmailIntelligence into scientific
pick 4c50fa3d23aaf1df001da9e26d50f068f8e2ece5 Resolve merge conflict and standardize scientific branch dependency handling
pick d560ac9dfb472973140e3c0f1c89d65613de7070 Resolve merge conflict and standardize scientific branch dependency handling
pick 9ffaeaceb47b0364b95211079db0e86e42f5db60 Enhance main branch dependency handling robustness
pick d4b565c529a44b090fe29ca58ac36cd7daa8f521 Enhance main branch dependency handling robustness
pick 157aa24cacf3cdc97b54412c982b397887c58f2a Standardize dependency handling in scientific branch
pick fcc5ef665e4a5b8e720055cdb8dd00392c4dbbdb Standardize dependency handling in scientific branch
pick 96efcd8885d2e3d1ac6235a1b92b2c4bc15c48d2 Update documentation to reflect conda environment support
pick 92e697d913a84c4af91e66d0fba3b7c01eaa01f0 Update documentation to reflect conda environment support
pick c6aa3fd9014aca7f4f08cff2feb195625cd1ad5c Update launcher guide to document conda environment support
pick 7270307351280f2bf64890f572712364cbae763a Update launcher guide to document conda environment support
pick 1ce17499d0a4eea5af2731867ebb5463354f4cff Add conda environment support to launch.py and restore launch.bat.new
pick 9450e0223144f66b4074af936c51f009dedaeb66 Add conda environment support to launch.py and restore launch.bat.new
pick e4a7cb060c131432985d5f0a5f0764fc04caf4ac Port validation features from main branch to scientific
pick 17bc8a19e1bf74cede5c3a8d93fa540480d0cffe Port validation features from main branch to scientific
pick 65f3f6d795734aa1a21eda9b21e0ff04b443e3eb Resolve redundant launcher scripts and consolidate to launch.py
pick 13fb2d6f135870e351c10f2ce8589b20e4dedce5 Resolve redundant launcher scripts and consolidate to launch.py
pick 14ea7fd3d3916f8eadd00e186d59bb05909c9f20 Consolidate launch scripts and enhance launcher functionality
pick 2c84bec9ede52fdf13ed7288ee833ce3b5eff23a Consolidate launch scripts and enhance launcher functionality
pick 798e9dfdb78eec4bbea337a7d3d876f4beed4979 Specify CPU wheels for torch to avoid NVIDIA dependencies
pick 365b39b79be91eceb6d1d3f8c02a33fdbe5c30c8 Specify CPU wheels for torch to avoid NVIDIA dependencies
pick fbcf9f99b61dbc6660c3fbbdb61534ba63f87945 Merge pull request #145 from MasumRab/fix/launch-bat-issues
pick 165a76bf3e9b38a7104e5d0ecc4041573378f3bd Merge pull request #145 from MasumRab/fix/launch-bat-issues
pick 9ec628b783c0ae06ccfb9d2b4382bd824a1d1dbc Merge branch 'scientific' into fix/launch-bat-issues
pick de3d067f5e6221e2fed0a25282fef2f231d70817 Merge branch 'scientific' into fix/launch-bat-issues
pick d608504f93b1117aa35adfec510d7a2fcdc738df Merge main into scientific: Prefer scientific branch for conflicts
pick 4d33318cf938cf519990fddd560b5463df27dc5d Merge main into scientific: Prefer scientific branch for conflicts
pick c7a02235cf187380e47fef6f50e74f323c50b422 Merge PR #149: Resolve merge conflicts in feat/gradio-layered-ui-foundation
pick 11f8ef18323ee067da16a926a68fd7140f5d1bf4 Merge PR #149: Resolve merge conflicts in feat/gradio-layered-ui-foundation
pick ccebe947b6fcdd85b61da76db40a36174df189c1 Resolve merge conflicts and address review comments in smart_filters.py
pick cac65e8684fe85060e14cc9dfb3e7c08fb11c5a4 Resolve merge conflicts and address review comments in smart_filters.py
pick 7e3d03eb9d79633b5d4d603565d85612bc1a0b54 Update AGENTS.md with architecture and codebase structure information
pick 18d6d60d719bfa01cb42958705282caa0c163a4d Update AGENTS.md with architecture and codebase structure information
pick 115254739c9b8620dcdfa739bc10b1ba081b8970 Merge pull request #151 from MasumRab/bug-bad-merges
pick 879392db1a5b576cb71ba197e169dbc5e556afef Merge pull request #151 from MasumRab/bug-bad-merges
pick 3e7d8e2e288a71d2eef3cddd0f7e4425c2062dd4 Merge branch 'scientific' into bug-bad-merges
pick c54dc45c6ee170b2e5ff82f0814a7fbd7cd64b18 Merge branch 'scientific' into bug-bad-merges
pick 31283174e4db11acc679b7f203ba5ecba02f1720 iflow changes
pick 9188a10478ac35204e2abd5122918cbf2e022520 iflow changes
pick c852877c606b1fa0bbd64ae9ef23faa5f9b8faf8 .gitattributes
pick ab7e6ecc6e93c5dd980021a22aa73d01cfed2546 .gitattributes
pick c558d84b5154de8488dc82b31f51a01aacab7809 Resolve merge conflicts in email_routes.py and protocols.py, and reinstate db update functions.
pick 9d1354faa50381e4dbcd1e79534fc7777f5a7091 Resolve merge conflicts in email_routes.py and protocols.py, and reinstate db update functions.
pick 31fcb754c0d958d157ad435c03d9dbb5b0eaa9d1 Fix merge conflicts and reinstate dataclass decorators and functions in launch.py, gmail_integration.py, and dependencies.py
pick 4f592c18839f654d08e6eae0178c39ddee9302cf Fix merge conflicts and reinstate dataclass decorators and functions in launch.py, gmail_integration.py, and dependencies.py
pick bf3e41e0b8fdbdef9e5dbd37dc45cb6147cf8a14 some merge fixes
pick eefbe33ad7baf0e9205a491cee2822cab7295529 some merge fixes
pick e159ce43609bc5cb0e4b96d9df7dc17f82a7cfba local changes Merge branch 'scientific' of https://github.com/MasumRab/EmailIntelligence into scientific
pick 2aaf39512aeb8f950177c9584b5f0f6838bbd4f1 local changes Merge branch 'scientific' of https://github.com/MasumRab/EmailIntelligence into scientific
pick 411937768ae265ce1b272968ee8c35963b7eca48 Update launch.py
pick 8ea3c8eb7a07cb8ebd8e358a18c577e84a6bf517 Update launch.py
pick 4741ac7f014df9c9a780f4a691cabc623bee607d Merge pull request #148 from MasumRab/branch_alignment_report
pick 5fa1849e39281d47e5fbc2fabd3bcc89aba303da Merge pull request #148 from MasumRab/branch_alignment_report
pick b433c55ff78ff3eca73979dc288b9fc2f95123af Resolve merge conflicts in feat/gradio-layered-ui-foundation
pick af9f731f4d1477c5e761a512cb2578f622929e02 Resolve merge conflicts in feat/gradio-layered-ui-foundation
pick 6f6622a1cb9ff3f267bf4ffa3e62690dde657bf1 iflow
pick 563608e8ffe16b99d6a419db6bd42ed5f2f1142c iflow
pick 431170b09455cabc3ca358d5e89dc22cb247d443 iflow md
pick bb13d6c7663e704f939232e6764e0fdd8d9db446 iflow md
pick daa7545f67606c0b28d10cd06233e4553afdf66b I have fixed the merge conflict in `branch_alignment_report.md` by removing the conflict markers and the redundant `Final Alignment Status` section.
pick 28390877209bf6b94ca6206bad7ee8632ed241c5 I have fixed the merge conflict in `branch_alignment_report.md` by removing the conflict markers and the redundant `Final Alignment Status` section.
pick f7db2f6562c2349dd6548c90ce41f36cdc8cacdb Merge remote-tracking branch 'origin/scientific' into scientific
pick 5928dc2329d82f79f0c788d340f99eb7e6ae71f5 Merge remote-tracking branch 'origin/scientific' into scientific
pick c340f43f4c1c6b19a2faf61f5082b106eed1ecfc Merge pull request #146 from MasumRab/fixes-branch
pick e8539d89c3e48a43c283e37cc555e90c5b9b9e6f Merge pull request #146 from MasumRab/fixes-branch
pick caad1792528bcb5abdc6aa9d4a9d658761c266d0 Resolve merge conflicts from main into fixes-branch
pick 853787da772aedf34173969b513b70e5f6fc88cd Resolve merge conflicts from main into fixes-branch
pick 452f258f73330471a6f2b10c7510cdb72be12d85 Potential fix for code scanning alert no. 21: Uncontrolled data used in path expression
pick a994462b787bc97f06bad7f6528dae10709b3ec8 Potential fix for code scanning alert no. 21: Uncontrolled data used in path expression
pick 2b0cedaf38b154a78ec1f1013a31dafc4d34a117 Merge branch 'fix/launch-bat-issues' of https://github.com/MasumRab/EmailIntelligence into fix/launch-bat-issues
pick 3f1df3796510481acfd01ebedd214e460664ff54 Merge branch 'fix/launch-bat-issues' of https://github.com/MasumRab/EmailIntelligence into fix/launch-bat-issues
pick 0c674760538de96a74d9d357bb6fa62d518a9066 Apply stashed changes: fix conflict markers and updates
pick c44124925ce29d824ee0cde838d5a3da01fedbcd Apply stashed changes: fix conflict markers and updates
pick 282c5dab378f4fae18d0da4eaad61837b17a05b5 cherry pick finished
pick 7b031b107c9057228edba1f1d22fb04d0b2bf5d7 cherry pick finished
pick c4aca2c109a4fafe0c6b1bd8dca3034d4a3d4676 Merge remote-tracking branch 'origin/fixes-branch' into fixes-branch
pick 3c0eec54a74d3e4594f64a51ec2ec67c1cd69683 Merge remote-tracking branch 'origin/fixes-branch' into fixes-branch
pick b854d3e2347f25c4cdd1ba3ff4fd74f4de1e207b Potential fix for code scanning alert no. 22: Uncontrolled data used in path expression
pick a48cfc91a36550b16570ea1a548f0b1de69bcc2a Potential fix for code scanning alert no. 22: Uncontrolled data used in path expression
pick d9768f73eae74bc4ec03109adb165d4521ecb85c Merge branch 'main' into refactor-data-source-abstraction2
pick 043ce3b20dd05a79b46d2f80ae69eafbed4c1b98 Merge branch 'main' into refactor-data-source-abstraction2
pick a4ab14d38b48c75d78b54fb19e7e408e72474c37 Update branch alignment report with final merge status
pick f94e4e1a1b7deb4b6eebace0b345752c9666f4d9 Update branch alignment report with final merge status
pick c12cef59286f8cdf3373133ec178b826806cb586 Merge branch 'fix/launch-bat-issues' of https://github.com/MasumRab/EmailIntelligence into fix/launch-bat-issues
pick 54bbfcac9c96c09a228cf6ed8e4957222a6a20a8 Merge branch 'fix/launch-bat-issues' of https://github.com/MasumRab/EmailIntelligence into fix/launch-bat-issues
pick ee319395b2000b93ab959f54b9724c6120719d48 Resolve merge conflicts from scientific branch
pick 71cf7e3b6d1654ee2218579647ab63015e4d0ef7 Resolve merge conflicts from scientific branch
pick 6ef32987f5e1ba6411719810d89d5a32e66a69e6 Merge branch 'fix/launch-bat-issues' of https://github.com/MasumRab/EmailIntelligence into fix/launch-bat-issues
pick d86109e7fdce7e71ee98ff1905d69d7ff75675a2 Merge branch 'fix/launch-bat-issues' of https://github.com/MasumRab/EmailIntelligence into fix/launch-bat-issues
pick 3143dbea2e69c6838df6a4ba92b93b66bbc0a590 Update performance metrics from recent test runs
pick 24f46e94e012cc1d8bfac4184522a6eddf4aedb6 Update performance metrics from recent test runs
pick 3a9df1ec27c8c75231d899dfadd3cc35d3bc7f61 Apply Black formatting to codebase
pick 4d9aab1faf667bd723f8ccd843011ddcd564c7b2 Apply Black formatting to codebase
pick 6f117efbc669483466ad3e5de104a59a33b3ec45 Merge pull request #142 from MasumRab/refactor-data-source-abstraction
pick 51d816fe61fa97e2973f22707a7c8870ede5ef53 Merge pull request #142 from MasumRab/refactor-data-source-abstraction
pick 2ea921f6ba24491d84ab0e50ab264762caf2b16b Potential fix for code scanning alert no. 22: Uncontrolled data used in path expression
pick 4e5da8b4a7a872c980e8e08275f79859a56d253a Potential fix for code scanning alert no. 22: Uncontrolled data used in path expression
pick 092ad9a4d833e35733e26bea48cf242f176171e7 Potential fix for code scanning alert no. 21: Uncontrolled data used in path expression
pick 9568dbbb3ad914fc54f265fabd6d7785ee7a309a Potential fix for code scanning alert no. 21: Uncontrolled data used in path expression
pick f4667472c9abc67041beb6b22c82ed980ea28203 Merge pull request #143 from MasumRab/fixes-branch
pick 7cd8c8e178f740f904d24ccca9ce6ab0df68ea95 Merge pull request #143 from MasumRab/fixes-branch
pick 19d52f1765d079bb102dc6f7fb2a359df77ee799 Add phased plan to attack major merge issues
pick 496629385b01080ee82de43e433cfa72916ef3b5 Add phased plan to attack major merge issues
pick a0a10d0a2af10deaface483f1818a1a385c6d5d2 Update cherry-pick progress: added 56a7f84, noted pervasive conflicts
pick e6d6af4fb22c0a6f4c0599ae602942e03756515b Update cherry-pick progress: added 0492a93, noted pervasive conflicts
pick 2b5ac78201bc5ae0fbd7feb66b3267ab95179933 Apply Black formatting to codebase
pick 651bd17bebb764f022a31bc047da399f56a86bb2 Apply Black formatting to codebase
pick 5ad25e7678d84e0acf8b582c5eb67abdb6ec09eb Fix merge conflicts and lint issues: resolve markers, fix pylint warnings
pick 52a5f4a934fd8510d7417dcabce70afe4a936cf3 Fix merge conflicts and lint issues: resolve markers, fix pylint warnings
pick 9f214aa0756d99784d114208685a44548b6e6722 Update report with cherry-pick progress
pick 7ee802c4f380b76c8aa11d43ae70ce942b0381bb Update report with cherry-pick progress
pick ddfa0eb4e2b2a46161e1d8e023b2419fc79fcbb7 Add restrictedpython dependency and clean performance metrics log
pick dda47e19fc3b88f4bcbb8d653f0c43fe01fc2003 Add restrictedpython dependency and clean performance metrics log
pick f51d7f3bebb1f5d832db537b27e77ef210df68b4 Add root redirect to Gradio UI and align with main branch goals
pick 91f71a44b743f6ccea74e1bbed2468ad880324d8 Add root redirect to Gradio UI and align with main branch goals
pick 8746a0c052c24ada826f37c5ea695d703f5485e9 Update performance metrics from recent test runs
pick 8189513d4447e49210678a78093538f49c81d69b Update performance metrics from recent test runs
pick 090fbcd2e85a26e09c002c17c2a179f939c28e2b Add uncherry-picked commits list to report
pick d1dfe55b68db224852d92dea9869013b6b4a9887 Add uncherry-picked commits list to report
pick b6ffbeabdef095e9400e808e73ffcb89840ec6bc Add RestrictedPython to dependencies to fix Gradio import error
pick aec66aca24728028075737c42a78c2f439e4a59b Add RestrictedPython to dependencies to fix Gradio import error
pick 2fc85a21a0e017414bf2028b6b312d1beae1897b Update branch alignment report with commit differences ordered by impact
pick 9dc7871bcf1af111a4832ffc70dbee2e6b66a7d2 Update branch alignment report with commit differences ordered by impact
pick 849264bd2ada0c68b429670cc8cc94661e59b3ff Add backend data files (categories, emails, settings, users)
pick 5e96119311a99e7e7fd081518580f226311a83af Add backend data files (categories, emails, settings, users)
pick bfabf81a4477828d6b84e73a23bec043b58db70a Merge branch 'main' of https://github.com/MasumRab/EmailIntelligence
