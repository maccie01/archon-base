import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/primitives/button';
import { Input } from '../ui/primitives/input';
import { Card } from '../ui/primitives/card';
import { AlertCircle, Key, Lock } from 'lucide-react';

export function LoginPage() {
  const [apiKey, setApiKey] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const { login, isAuthenticated, error: authError } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as any)?.from?.pathname || '/';

  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    if (!apiKey.trim()) {
      setLocalError('Please enter an API key');
      return;
    }

    setIsSubmitting(true);

    try {
      await login(apiKey);
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const errorMessage = localError || authError;

  return (
    <div className="min-h-screen bg-white dark:bg-black flex items-center justify-center">
      {/* Background Grid Effect */}
      <div className="fixed inset-0 neon-grid pointer-events-none z-0" />

      {/* Login Card */}
      <div className="relative w-full max-w-md px-6 z-10">
        <Card
          blur="md"
          transparency="light"
          size="lg"
          className="w-full"
        >
          {/* Logo and Header */}
          <div className="flex flex-col items-center gap-6 mb-8">
            <div className="relative">
              <div className="absolute inset-0 bg-blue-500/20 blur-2xl rounded-full"></div>
              <img
                src="/logo-neon.png"
                alt="Archon"
                className="w-20 h-20 relative z-10"
              />
            </div>
            <div className="text-center">
              <h1 className="text-3xl font-bold text-foreground mb-2">
                Welcome to Archon
              </h1>
              <p className="text-muted-foreground">
                Enter your API key to continue
              </p>
            </div>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* API Key Input */}
            <div className="space-y-2">
              <label htmlFor="apiKey" className="block text-sm font-medium text-foreground">
                API Key
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Key className="h-5 w-5 text-muted-foreground" />
                </div>
                <Input
                  id="apiKey"
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Enter your API key"
                  className="pl-10"
                  disabled={isSubmitting}
                  autoFocus
                  autoComplete="off"
                />
              </div>
            </div>

            {/* Error Message */}
            {errorMessage && (
              <div className="flex items-start gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800/50">
                <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-sm text-red-700 dark:text-red-300">
                    {errorMessage}
                  </p>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              className="w-full"
              loading={isSubmitting}
              disabled={isSubmitting || !apiKey.trim()}
            >
              <Lock className="h-4 w-4 mr-2" />
              {isSubmitting ? 'Authenticating...' : 'Login'}
            </Button>
          </form>

          {/* Help Text */}
          <div className="mt-6 pt-6 border-t border-border">
            <p className="text-sm text-muted-foreground text-center">
              Need an API key? Contact your administrator or check the documentation.
            </p>
          </div>
        </Card>

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="text-sm text-muted-foreground">
            Secured by Archon Authentication
          </p>
        </div>
      </div>
    </div>
  );
}
