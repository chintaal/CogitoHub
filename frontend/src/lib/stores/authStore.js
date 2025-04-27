import { writable } from 'svelte/store';

// Create stores for user and profiles
export const user = writable(null);
const profiles = writable(new Map());

// Load user data from localStorage on initialization
const savedUser = localStorage.getItem('cogitohub_user');
if (savedUser) {
    user.set(JSON.parse(savedUser));
}

// Save user data to localStorage when it changes
user.subscribe(value => {
    if (value) {
        localStorage.setItem('cogitohub_user', JSON.stringify(value));
    } else {
        localStorage.removeItem('cogitohub_user');
    }
});

// Mock login function - in a real app this would validate credentials
export async function login(email, password) {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const mockUser = {
        uid: 'user-' + Math.random().toString(36).substr(2, 9),
        email,
        displayName: email.split('@')[0],
        photoURL: `https://ui-avatars.com/api/?name=${encodeURIComponent(email.split('@')[0])}`
    };
    
    user.set(mockUser);
    return mockUser;
}

// Add logout function
export async function logout() {
    user.set(null);
    localStorage.removeItem('cogitohub_user');
    localStorage.removeItem('cogitohub_profiles');
    return true;
}

// Get user profile
export async function getUserProfile(uid) {
    let userProfiles;
    profiles.subscribe(value => userProfiles = value)();
    
    if (userProfiles.has(uid)) {
        return userProfiles.get(uid);
    }
    
    // If no profile exists, return null to trigger onboarding
    return null;
}

// Update user profile
export async function updateUserProfile(uid, profileData) {
    try {
        profiles.update(profiles => {
            profiles.set(uid, {
                ...profiles.get(uid),
                ...profileData,
                updatedAt: new Date().toISOString()
            });
            return profiles;
        });
        
        // Save profiles to localStorage
        const userProfiles = {};
        profiles.subscribe(value => {
            value.forEach((profile, key) => {
                userProfiles[key] = profile;
            });
        })();
        localStorage.setItem('cogitohub_profiles', JSON.stringify(userProfiles));
        
        return { success: true };
    } catch (error) {
        console.error('Error updating profile:', error);
        return { success: false, error };
    }
}

// Load saved profiles from localStorage on initialization
const savedProfiles = localStorage.getItem('cogitohub_profiles');
if (savedProfiles) {
    const parsedProfiles = JSON.parse(savedProfiles);
    const profileMap = new Map();
    Object.entries(parsedProfiles).forEach(([key, value]) => {
        profileMap.set(key, value);
    });
    profiles.set(profileMap);
}