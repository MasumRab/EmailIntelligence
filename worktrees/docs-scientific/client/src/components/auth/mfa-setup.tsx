import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/hooks/use-auth';
import { toast } from 'sonner';

export function MFASetup() {
  const { mfaSetup, setupMFA, enableMFA } = useAuth();
  const [token, setToken] = useState('');

  const handleSetup = async () => {
    const result = await setupMFA();
    if (!result.success) {
      toast.error(result.error || 'Failed to setup MFA');
    }
  };

  const handleEnable = async () => {
    const result = await enableMFA(token);
    if (result.success) {
      toast.success('MFA enabled successfully');
      // Reset the MFA setup state
    } else {
      toast.error(result.error || 'Failed to enable MFA');
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Setup Two-Factor Authentication</CardTitle>
        <CardDescription>Secure your account with an authenticator app</CardDescription>
      </CardHeader>
      <CardContent>
        {!mfaSetup ? (
          <div className="space-y-4">
            <p>Click the button below to setup two-factor authentication with an authenticator app like Google Authenticator or Authy.</p>
            <Button onClick={handleSetup} className="w-full">
              Setup MFA
            </Button>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="text-center">
              <p className="mb-4">Scan the QR code below with your authenticator app:</p>
              {mfaSetup.qr_code && (
                <div className="flex justify-center">
                  <img 
                    src={`data:image/png;base64,${mfaSetup.qr_code}`} 
                    alt="MFA QR Code" 
                    className="max-w-xs border rounded p-2 bg-white"
                  />
                </div>
              )}
            </div>
            
            <div>
              <p className="mb-2">Or enter this secret key manually:</p>
              <div className="bg-gray-100 p-3 rounded text-center font-mono break-all">
                {mfaSetup.secret}
              </div>
            </div>
            
            <div>
              <label htmlFor="mfa-token" className="block text-sm font-medium text-gray-700 mb-1">
                Enter Code from Authenticator App
              </label>
              <Input
                id="mfa-token"
                type="text"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                required
                placeholder="Enter 6-digit code"
              />
            </div>
            
            <div>
              <p className="text-sm text-gray-600 mb-2">Your backup codes (save these in a secure place):</p>
              <div className="bg-gray-100 p-3 rounded grid grid-cols-2 gap-2">
                {mfaSetup.backup_codes.map((code, index) => (
                  <div key={index} className="font-mono text-center text-sm p-1 bg-white rounded">
                    {code}
                  </div>
                ))}
              </div>
            </div>
            
            <Button onClick={handleEnable} className="w-full">
              Enable MFA
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}