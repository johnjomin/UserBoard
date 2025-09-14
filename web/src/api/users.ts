export interface User {
  id: number;
  firstname: string;
  lastname: string;
  age: number;
  date_of_birth: string;
}

export interface UserCreate {
  firstname: string;
  lastname: string;
  age: number;
  date_of_birth: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const usersApi = {
  async getAll(): Promise<User[]> {
    const response = await fetch(`${API_BASE_URL}/users`);
    if (!response.ok) {
      throw new Error('Failed to fetch users');
    }
    return response.json();
  },

  async create(user: UserCreate): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user),
    });
    if (!response.ok) {
      throw new Error('Failed to create user');
    }
    return response.json();
  },

  async delete(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/user`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id }),
    });
    if (!response.ok) {
      throw new Error('Failed to delete user');
    }
  }
};