import { defineStore } from 'pinia'
import type { User } from '@/types/User'
import router from '@/router'
import type { Token } from '@/types/Token'

const base_api_url = import.meta.env.VITE_BASE_API_URL

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as User | null,
        token: null as Token | null,
        isLoading: false
    }),
    actions: {
        async login(username: string, password: string, redirect = '/') {
            this.isLoading = true
            try {
                // Request token
                const tokenResponse = await fetch(`${base_api_url}/auth/token`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams({
                        username,
                        password
                    }).toString()
                });

                if (!tokenResponse.ok) {
                    throw new Error('Failed to login');
                }

                const tokenData: Token = await tokenResponse.json();
                this.token = tokenData;
                localStorage.setItem('token', JSON.stringify(this.token));

                // Fetch user data
                const userResponse = await fetch(`${base_api_url}/auth/me`, {
                    method: 'GET',
                    headers: {
                        Authorization: `Bearer ${this.token.access_token}`
                    }
                });

                if (!userResponse.ok) {
                    throw new Error('Failed to fetch user data');
                }

                const userData: User = await userResponse.json();
                this.user = userData;
                router.push(redirect);
            } catch (error) {
                console.error('Login failed:', error);
                throw error;
            } finally {
                this.isLoading = false;
            }
        },

        async register(email: string, password: string, firstName: string, lastName: string, redirect = '/') {
            this.isLoading = true;
            try {
                const response = await fetch(`${base_api_url}/auth/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email,
                        password,
                        first_name: firstName,
                        last_name: lastName
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to register');
                }

                await this.login(email, password, redirect);
            } catch (error) {
                console.error('Registration failed:', error);
                throw error;
            } finally {
                this.isLoading = false;
            }
        },
        async updateUser(id: string, first_name: string, last_name: string, email: string) {
            try {
                const response = await fetch(`${base_api_url}/users/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${this.token?.access_token}`
                    },
                    body: JSON.stringify({
                        first_name: first_name,
                        last_name: last_name,
                        email: email
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to update user');
                }

                await this.fetchUser();
            } catch (error) {
                console.error('Failed to update user:', error);
                throw error;
            }
        },

        logout() {
            this.user = null;
            this.token = null;
            localStorage.removeItem('token');
            router.push('/');
        },

        async fetchUser() {
            try {
                const storedToken = localStorage.getItem('token');
                if (storedToken) {
                    this.token = JSON.parse(storedToken);

                    if (!this.token) {
                        throw new Error('No token found');
                    }

                    const userResponse = await fetch(`${base_api_url}/auth/me`, {
                        method: 'GET',
                        headers: {
                            Authorization: `Bearer ${this.token.access_token}`
                        }
                    });

                    if (!userResponse.ok) {
                        throw new Error('Failed to fetch user data');
                    }

                    const userData: User = await userResponse.json();
                    this.user = userData;
                }
            } catch (error) {
                console.error('Failed to fetch user:', error);
                this.logout();
            }
        }
    }
});