import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/hooks/use-auth';
import { toast } from 'sonner';

export function MFADisable() {
  const { disableMFA } = useAuth();

  const handleDisable = async () => {
    const result = await disableMFA();
    if (result.success) {
      toast.success('MFA disabled successfully');
    } else {
      toast.error(result.error || 'Failed to disable MFA');
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Disable Two-Factor Authentication</CardTitle>
        <CardDescription>Turn off two-factor authentication for your account</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <p>Are you sure you want to disable two-factor authentication? This will reduce the security of your account.</p>
          <Button onClick={handleDisable} variant="destructive" className="w-full">
            Disable MFA
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}