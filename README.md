# Biosecurity
Flask Python Web App functioning as a biosecurity guide, providing information on bee pests and diseases present in New Zealand, as well as those that are not currently found in the country.

## Introduction

This Bee Pest/Disease Guide Management System is designed to support the needs of Apiarists, Staff, and Administrators, providing tailored access and functionality depending on the user's role. The system facilitates the management of user profiles, the bee pest/disease guide, and offers comprehensive role-based access control to ensure users can only access appropriate information and functionalities.

## Features

### Role-Based Access Control (RBAC)

The system defines three primary user roles:
- **Apiarists**: Users with this role can manage their own profiles and have access to the bee pest/disease guide, including detailed information on each pest/disease.
- **Staff**: In addition to managing their own profiles, Staff users can view Apiarist profiles, manage the guide's content (add, update, delete entries), and handle image uploads, including setting primary images.
- **Administrators**: Admins have full system access, including user management (Apiarists and Staff) and complete control over the guide's content.

### User Profile Management

- **Update Personal Information**: Users can update their personal information, including contact details.
- **Change Password**: A feature allowing users to change their account password for security purposes.

### Bee Pest/Disease Guide

- **View Guide**: Accessible by Apiarists and higher roles, showcasing primary images, common names, and presence status in NZ.
- **Manage Guide**: Staff and Administrators can add, update, or delete guide entries, including detailed pest/disease information and images.

