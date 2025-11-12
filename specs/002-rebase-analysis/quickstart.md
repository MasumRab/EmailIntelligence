# Quickstart Guide: Orchestration Tools Verification and Review        
                                                                       
## Prerequisites                                                       
                                                                       
- Python 3.11+                                                         
- Git 2.0+                                                             
- Access to Git repository with orchestration tools                    
- API key for the verification system (obtained from system administrat
or)                                                                    
                                                                       
## Installation                                                        
                                                                       
1. Clone the orchestration tools repository:                           
   ```bash                                                             
   git clone <repository-url>                                          
   cd <repository-directory>                                           
   ```                                                                 
                                                                       
2. Install Python dependencies:                                        
   ```bash                                                             
   pip install -r requirements.txt                                     
   # Or if no requirements file exists:                                
   pip install gitpython pyyaml requests cryptography pygithub         
   ```                                                                 
                                                                       
3. Configure the verification system:                                  
   ```bash                                                             
   # Copy configuration template                                       
   cp config/verification_profiles.yaml.example config/verification_pro
files.yaml                                                             
   cp config/auth_config.yaml.example config/auth_config.yaml          
   ```                                                                 
                                                                       
4. Set up Git hooks (optional, for automated verification):            
   ```bash                                                             
   cp scripts/pre-commit-hook.sh .git/hooks/pre-commit                 
   chmod +x .git/hooks/pre-commit                                      
   ```                                                                 
                                                                       
## Configuration                                                       
                                                                       
### Authentication Setup                                               
1. Set your API key in `config/auth_config.yaml`:                      
   ```yaml                                                             
   api_key: your-encrypted-api-key                                     
   role: RUN  # Options: READ, RUN, REVIEW, ADMIN                      
   ```                                                                 
                                                                       
### Verification Profiles                                              
1. Configure verification profiles in `config/verification_profiles.yam
l`:                                                                    
   ```yaml                                                             
   main-branch:                                                        
     required_checks:                                                  
       - "context-check"                                               
       - "dependency-validation"                                       
       - "compatibility-check"                                         
     optional_checks:                                                  
       - "performance-check"                                           
     context_requirements:                                             
       - "environment-variables"                                       
       - "configuration-files"                                         
                                                                       
   scientific-branch:                                                  
     required_checks:                                                  
       - "context-check"                                               
       - "dependency-validation"                                       
     context_requirements:                                             
       - "environment-variables"                                       
     branch_specific_rules:                                            
       - "double_review_required"                                      
   ```                                                                 
                                                                       
## Basic Usage                                                         
                                                                       
### Run Verification Manually                                          
```bash                                                                
# Run verification for current branch against main                     
python -m orchestration-tools.src.cli.orchestration_cli verify --source
-branch $(git branch --show-current) --target-branch main              
                                                                       
# Run verification for specific branch pair                            
python -m orchestration-tools.src.cli.orchestration_cli verify --source
-branch feature-branch --target-branch scientific                      
                                                                       
# Run with specific verification profile                               
python -m orchestration-tools.src.cli.orchestration_cli verify --profil
e scientific-branch --source-branch feature-x --target-branch scientifi
c                                                                      
```                                                                    
                                                                       
### Check Verification Status                                          
```bash                                                                
# Check status of latest verification for current branch               
python -m orchestration-tools.src.cli.orchestration_cli status --branch
 $(git branch --show-current)                                          
                                                                       
# Check status for specific verification                               
python -m orchestration-tools.src.cli.orchestration_cli status --verifi
cation-id <verification-id>                                            
```                                                                    
                                                                       
### Approve Verification Results (Reviewers only)                      
```bash                                                                
# Approve a verification result                                        
python -m orchestration-tools.src.cli.orchestration_cli approve --verif
ication-id <verification-id> --comment "Approved after review"         
                                                                       
# Reject a verification result                                         
python -m orchestration-tools.src.orchestration_cli reject --verificati
on-id <verification-id> --comment "Changes need modification"          
```                                                                    
                                                                       
## API Usage                                                           
                                                                       
### Submit Verification Request                                        
```bash                                                                
curl -X POST https://verification-system.example.com/api/v1/verify \   
  -H "Authorization: Bearer YOUR_API_KEY" \                            
  -H "Content-Type: application/json" \                                
  -d '{                                                                
    "source_branch": "feature-branch",                                 
    "target_branch": "main",                                           
    "profile": "main-branch"                                           
  }'                                                                   
```                                                                    
                                                                       
### Get Verification Status                                            
```bash                                                                
curl -X GET https://verification-system.example.com/api/v1/verify/VERIF
ICATION_ID \                                                           
  -H "Authorization: Bearer YOUR_API_KEY"                              
```                                                                    
                                                                       
## Common Scenarios                                                    
                                                                       
### Scenario 1: Developer Merging to Main Branch                       
1. Make changes to orchestration tools                                 
2. Run local verification against main:                                
   ```bash                                                             
   python -m orchestration-tools.src.cli.orchestration_cli verify --sou
rce-branch feature --target-branch main                                
   ```                                                                 
3. Address any issues flagged by verification                          
4. Request review from designated reviewer                             
5. Await approval before merging                                       
                                                                       
### Scenario 2: Reviewer Approving Verification                        
1. Receive notification of pending verification                        
2. Review verification report in UI or CLI                             
3. Validate that all required checks passed                            
4. Approve verification:                                               
   ```bash                                                             
   python -m orchestration-tools.src.cli.orchestration_cli approve --ve
rification-id <id> --comment "Approved after review"                   
   ```                                                                 
                                                                       
### Scenario 3: Handling Verification Failures                         
1. Receive notification of verification failure                        
2. Examine detailed report to identify issues                          
3. Generate remediation steps                                          
4. Update orchestration tools to address issues                        
5. Re-run verification                                                 
                                                                       
## Troubleshooting                                                     
                                                                       
### Verification Times Out                                             
- Check if all required external services are accessible               
- Verify that context requirements (env vars, configs) are properly set
- Review the verification profile for excessive checks                 
                                                                       
### API Authentication Fails                                           
- Verify API key is correctly configured                               
- Confirm role permissions match required operations                   
- Check system time is synchronized (for token validation)             
                                                                       
### Git Integration Issues                                             
- Ensure Git hooks are properly installed                              
- Verify Git configuration allows hook execution                       
- Check that the hook script has execution permissions                 
                                                                       
## Next Steps                                                          
                                                                       
1. Review the detailed [Verification Guide](verification_guide.md) for 
advanced usage                                                         
2. Set up automated notifications for verification results             
3. Customize verification profiles for your specific branch types      
4. Integrate with your existing CI/CD pipeline