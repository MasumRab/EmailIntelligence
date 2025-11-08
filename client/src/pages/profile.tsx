import { UserProfile } from '@/components/auth/user-profile';

export default function ProfilePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">User Profile</h1>
          <p className="text-gray-600 mt-2">Manage your account settings and security</p>
        </div>
        <UserProfile />
      </div>
    </div>
  );
}