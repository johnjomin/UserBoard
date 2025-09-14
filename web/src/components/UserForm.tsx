import React, { useState } from 'react';
import { UserCreate } from '../api/users';

interface UserFormProps {
  onSubmit: (user: UserCreate) => Promise<void>;
  loading: boolean;
}

export const UserForm: React.FC<UserFormProps> = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState<UserCreate>({
    firstname: '',
    lastname: '',
    age: 0,
    date_of_birth: '',
  });
  const [errors, setErrors] = useState<Partial<UserCreate>>({});

  const validateForm = (): boolean => {
    const newErrors: Partial<UserCreate> = {};

    if (!formData.firstname.trim()) {
      newErrors.firstname = 'First name is required';
    }

    if (!formData.lastname.trim()) {
      newErrors.lastname = 'Last name is required';
    }

    if (formData.age <= 0 || formData.age > 150) {
      newErrors.age = 'Age must be between 1 and 150';
    }

    if (!formData.date_of_birth) {
      newErrors.date_of_birth = 'Date of birth is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      await onSubmit({
        ...formData,
        firstname: formData.firstname.trim(),
        lastname: formData.lastname.trim(),
      });
      
      // Reset form on success
      setFormData({
        firstname: '',
        lastname: '',
        age: 0,
        date_of_birth: '',
      });
      setErrors({});
    } catch (error) {
      console.error('Failed to create user:', error);
    }
  };

  const handleChange = (field: keyof UserCreate, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <div className="form-container">
      <h2>Add New User</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="firstname">First Name</label>
            <input
              id="firstname"
              type="text"
              value={formData.firstname}
              onChange={(e) => handleChange('firstname', e.target.value)}
              disabled={loading}
            />
            {errors.firstname && <div className="error">{errors.firstname}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="lastname">Last Name</label>
            <input
              id="lastname"
              type="text"
              value={formData.lastname}
              onChange={(e) => handleChange('lastname', e.target.value)}
              disabled={loading}
            />
            {errors.lastname && <div className="error">{errors.lastname}</div>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="age">Age</label>
            <input
              id="age"
              type="number"
              value={formData.age}
              onChange={(e) => handleChange('age', parseInt(e.target.value) || 0)}
              min="1"
              max="150"
              disabled={loading}
            />
            {errors.age && <div className="error">{errors.age}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="date_of_birth">Date of Birth</label>
            <input
              id="date_of_birth"
              type="date"
              value={formData.date_of_birth}
              onChange={(e) => handleChange('date_of_birth', e.target.value)}
              disabled={loading}
            />
            {errors.date_of_birth && <div className="error">{errors.date_of_birth}</div>}
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Adding...' : 'Add User'}
        </button>
      </form>
    </div>
  );
};