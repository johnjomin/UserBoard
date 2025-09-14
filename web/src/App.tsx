import React, { useState, useEffect } from 'react';
import { UserForm } from './components/UserForm';
import { UserList } from './components/UserList';
import { User, UserCreate, usersApi } from './api/users';

function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const fetchedUsers = await usersApi.getAll();
      setUsers(fetchedUsers);
    } catch (error) {
      console.error('Failed to fetch users:', error);
      alert('Failed to load users. Please refresh the page.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (userData: UserCreate) => {
    setCreateLoading(true);
    try {
      const newUser = await usersApi.create(userData);
      setUsers(prev => [...prev, newUser]);
    } catch (error) {
      console.error('Failed to create user:', error);
      alert('Failed to create user. Please try again.');
      throw error; // Re-throw to let form handle it
    } finally {
      setCreateLoading(false);
    }
  };

  const handleDeleteUser = async (id: number) => {
    try {
      await usersApi.delete(id);
      setUsers(prev => prev.filter(user => user.id !== id));
    } catch (error) {
      console.error('Failed to delete user:', error);
      throw error; // Re-throw to let component handle it
    }
  };

  // Load users on component mount
  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <>
      <header className="header">
        <div className="container">
          <h1>UserBoard</h1>
        </div>
      </header>
      
      <div className="container">
        <UserForm onSubmit={handleCreateUser} loading={createLoading} />
        <UserList 
          users={users} 
          loading={loading} 
          onDelete={handleDeleteUser} 
        />
      </div>
    </>
  );
}

export default App;