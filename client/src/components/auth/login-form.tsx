import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/hooks/use-auth';
import { toast } from 'sonner';

export function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mfaToken, setMfaToken] = useState('');
  const [showMfaInput, setShowMfaInput] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
<<<<<<< HEAD
    
    const result = await login(username, password, showMfaInput ? mfaToken : undefined);
    
=======

    const result = await login(username, password, showMfaInput ? mfaToken : undefined);

>>>>>>> 3809f0f3a2e942466dc0ff196cd81b50bb948e4c
    if (result.success) {
      if (result.mfaRequired) {
        setShowMfaInput(true);
        toast.info('MFA token required. Please enter your authenticator code.');
      } else {
        window.location.href = '/dashboard'; // Redirect to dashboard after successful login
      }
    } else {
      toast.error(result.error || 'Login failed');
    }
  };

  const handleMfaSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
<<<<<<< HEAD
    
    const result = await login(username, password, mfaToken);
    
=======

    const result = await login(username, password, mfaToken);

>>>>>>> 3809f0f3a2e942466dc0ff196cd81b50bb948e4c
    if (result.success) {
      window.location.href = '/dashboard'; // Redirect to dashboard after successful MFA verification
    } else {
      toast.error(result.error || 'MFA verification failed');
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Login</CardTitle>
        <CardDescription>Enter your credentials to access the Email Intelligence Platform</CardDescription>
      </CardHeader>
      <CardContent>
        {!showMfaInput ? (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                placeholder="Enter your username"
              />
            </div>
<<<<<<< HEAD
            
=======

>>>>>>> 3809f0f3a2e942466dc0ff196cd81b50bb948e4c
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Enter your password"
              />
            </div>
<<<<<<< HEAD
            
=======

>>>>>>> 3809f0f3a2e942466dc0ff196cd81b50bb948e4c
            <Button type="submit" className="w-full">
              Login
            </Button>
          </form>
        ) : (
          <form onSubmit={handleMfaSubmit} className="space-y-4">
            <div>
              <label htmlFor="mfa-token" className="block text-sm font-medium text-gray-700 mb-1">
                MFA Code
              </label>
              <Input
                id="mfa-token"
                type="text"
                value={mfaToken}
                onChange={(e) => setMfaToken(e.target.value)}
                required
                placeholder="Enter your authenticator code"
              />
            </div>
<<<<<<< HEAD
            
            <Button type="submit" className="w-full">
              Verify MFA
            </Button>
            
            <Button 
              type="button" 
              variant="outline" 
=======

            <Button type="submit" className="w-full">
              Verify MFA
            </Button>

            <Button
              type="button"
              variant="outline"
>>>>>>> 3809f0f3a2e942466dc0ff196cd81b50bb948e4c
              className="w-full"
              onClick={() => setShowMfaInput(false)}
            >
              Use Different Account
            </Button>
          </form>
        )}
      </CardContent>
    </Card>
  );
}