import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getApiUrl } from '../config/api';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (apiKey: string) => Promise<void>;
  logout: () => void;
  getApiKey: () => string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_KEY_STORAGE_KEY = 'archon_api_key';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const getApiKey = useCallback(() => {
    return localStorage.getItem(API_KEY_STORAGE_KEY);
  }, []);

  const validateApiKey = useCallback(async (apiKey: string): Promise<boolean> => {
    try {
      const baseUrl = getApiUrl();
      const response = await fetch(`${baseUrl}/api/auth/validate`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        return true;
      }

      if (response.status === 401) {
        return false;
      }

      throw new Error(`Validation failed with status: ${response.status}`);
    } catch (error) {
      console.error('API key validation error:', error);
      throw error;
    }
  }, []);

  const login = useCallback(async (apiKey: string) => {
    setError(null);
    setIsLoading(true);

    try {
      const isValid = await validateApiKey(apiKey);

      if (isValid) {
        localStorage.setItem(API_KEY_STORAGE_KEY, apiKey);
        setIsAuthenticated(true);
        setError(null);
      } else {
        setError('Invalid API key. Please check your key and try again.');
        throw new Error('Invalid API key');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Authentication failed';
      setError(errorMessage);
      setIsAuthenticated(false);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [validateApiKey]);

  const logout = useCallback(() => {
    localStorage.removeItem(API_KEY_STORAGE_KEY);
    setIsAuthenticated(false);
    setError(null);
  }, []);

  useEffect(() => {
    const initAuth = async () => {
      const storedKey = getApiKey();

      if (!storedKey) {
        setIsAuthenticated(false);
        setIsLoading(false);
        return;
      }

      try {
        const isValid = await validateApiKey(storedKey);
        setIsAuthenticated(isValid);

        if (!isValid) {
          localStorage.removeItem(API_KEY_STORAGE_KEY);
        }
      } catch (error) {
        console.error('Failed to validate stored API key:', error);
        setIsAuthenticated(false);
        localStorage.removeItem(API_KEY_STORAGE_KEY);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, [getApiKey, validateApiKey]);

  const value: AuthContextType = {
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    getApiKey,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
