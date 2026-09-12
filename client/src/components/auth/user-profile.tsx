import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { MFASetup } from '@/components/auth/mfa-setup';
import { MFADisable } from '@/components/auth/mfa-disable';

export function UserProfile() {
  const [showMfaSetup, setShowMfaSetup] = useState(false);
  const [showMfaDisable, setShowMfaDisable] = useState(false);
  // In a real implementation, you would get the user's MFA status from the server
  const mfaEnabled = false; // Placeholder

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>User Profile</CardTitle>
          <CardDescription>Manage your account settings</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium">Account Information</h3>
              <p className="text-gray-600">Username: user@example.com</p>
              <p className="text-gray-600">Role: User</p>
            </div>

            <div>
              <h3 className="text-lg font-medium">Security Settings</h3>
              {mfaEnabled ? (
                <div className="space-y-4">
                  <p className="text-green-600">Two-factor authentication is enabled</p>
                  <Button onClick={() => setShowMfaDisable(true)} variant="outline">
                    Disable MFA
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <p>Two-factor authentication is not enabled</p>
                  <Button onClick={() => setShowMfaSetup(true)}>
                    Enable MFA
                  </Button>
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {showMfaSetup && (
        <MFASetup />
      )}

      {showMfaDisable && (
        <MFADisable />
      )}
    </div>
  );
}