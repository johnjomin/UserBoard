import React from 'react';
import { User } from '../api/users';

interface UserListProps {
  users: User[];
  loading: boolean;
  onDelete: (id: number) => Promise<void>;
}

export const UserList: React.FC<UserListProps> = ({ users, loading, onDelete }) => {
  const handleDelete = async (id: number, fullName: string) => {
    if (window.confirm(`Are you sure you want to delete ${fullName}?`)) {
      try {
        await onDelete(id);
      } catch (error) {
        console.error('Failed to delete user:', error);
        alert('Failed to delete user. Please try again.');
      }
    }
  };

  if (loading) {
    return <div className="loading">Loading users...</div>;
  }

  return (
    <div className="users-container">
      <h2>Users ({users.length})</h2>
      
      {users.length === 0 ? (
        <div className="no-users">No users found. Add some users using the form above.</div>
      ) : (
        <table className="users-table">
          <thead>
            <tr>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Age</th>
              <th>Date of Birth</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.firstname}</td>
                <td>{user.lastname}</td>
                <td>{user.age}</td>
                <td>{new Date(user.date_of_birth).toLocaleDateString()}</td>
                <td>
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDelete(user.id, `${user.firstname} ${user.lastname}`)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};