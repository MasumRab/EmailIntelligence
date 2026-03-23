import { useState, useEffect } from 'react';

interface User {
  username: string;
  role: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface MFASetupResponse {
  secret: string;
  qr_code: string;
  backup_codes: string[];
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [mfaRequired, setMfaRequired] = useState(false);
  const [mfaSetup, setMfaSetup] = useState<MFASetupResponse | null>(null);

  useEffect(() => {
    // Check if user is already authenticated
    const token = localStorage.getItem('access_token');
    if (token) {
      // In a real app, you'd verify the token with the server
      // For now, we'll just check if it exists
      setIsLoading(false);
      // You would typically fetch user info here
      // setUser({ username: 'user', role: 'user' });
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (username: string, password: string, mfaToken?: string) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username, 
          password,
          mfa_token: mfaToken
        }),
      });

      if (response.ok) {
        const data: LoginResponse = await response.json();
        localStorage.setItem('access_token', data.access_token);
        // You would typically fetch user info here
        setUser({ username, role: 'user' });
        setMfaRequired(false);
        return { success: true };
      } else if (response.status === 401) {
        const headers = response.headers;
        if (headers.get('X-MFA-Required') === 'true') {
          setMfaRequired(true);
          return { success: false, mfaRequired: true };
        }
      }
      
      const errorData = await response.json();
      return { success: false, error: errorData.detail || 'Login failed' };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const setupMFA = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/auth/mfa/setup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data: MFASetupResponse = await response.json();
        setMfaSetup(data);
        return { success: true, data };
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.detail || 'Failed to setup MFA' };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const enableMFA = async (token: string) => {
    try {
      const accessToken = localStorage.getItem('access_token');
      const response = await fetch('/api/auth/mfa/enable', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ token }),
      });

      if (response.ok) {
        setMfaSetup(null);
        return { success: true };
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.detail || 'Failed to enable MFA' };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const disableMFA = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/auth/mfa/disable', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        return { success: true };
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.detail || 'Failed to disable MFA' };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  return {
    user,
    isLoading,
    mfaRequired,
    mfaSetup,
    login,
    logout,
    setupMFA,
    enableMFA,
    disableMFA,
  };
}