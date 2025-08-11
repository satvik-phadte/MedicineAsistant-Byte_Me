# Medicine Assistant App–API Contract.

## This is the official contract between the frontend,backend for all API communication and data models.
## Includes integrations with Google Maps API (for pharmacy location search) and OCR API (for prescription text extraction).

Core Features
User Authentication & Role Management (Customer, Doctor, Pharmacy)
Medicine Search with Pharmacy Stock (Google Maps integration for geolocation)
Prescription Upload & OCR Processing
Medicine Reminders with Notifications
Doctor Prescription Management
Pharmacy Inventory Management

| Model            | Fields                                                                                                                       |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **User**         | `id`, `role`, `name`, `email`, `password`, `phone`, `address`                                                                |
| **Medicine**     | `id`, `name`, `brand`, `description`, `price`, `stock`, `pharmacy_id`                                                        |
| **Prescription** | `id`, `user_id`, `doctor_id`, `pharmacy_id`, `medicines[] (medicine_id, dosage, duration)`, `uploaded_image_url`, `ocr_text` |
| **Reminder**     | `id`, `user_id`, `medicine_name`, `time (ISO 8601)`, `repeat`                                                                | 



| Feature                                  | HTTP Method | Endpoint Path                                               | Description                                                                                     | Request Body                                      | Success Response                                                         | Error Response |
| ---------------------------------------- | ----------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------ | -------------- |
| **Register User**                        | POST        | `/api/auth/register`                                        | Register a new user (customer, doctor, pharmacy)                                                | `{ role, name, email, password, phone, address }` | `{ message, user_id }`                                                   | `{ error }`    |
| **Login User**                           | POST        | `/api/auth/login`                                           | Login and return JWT token                                                                      | `{ email, password }`                             | `{ token, role, user_id }`                                               | `{ error }`    |
| **Search Medicine**                      | GET         | `/api/medicines/search?name={medicine}&lat={lat}&lng={lng}` | Search nearby pharmacies for a specific medicine using **Google Maps API** location coordinates | N/A                                               | `[ { pharmacy_id, pharmacy_name, address, price, stock, distance_km } ]` | `{ error }`    |
| **Upload Prescription (OCR)**            | POST        | `/api/prescriptions/upload`                                 | Upload prescription image and extract text using **OCR API**                                    | `multipart/form-data: { file, user_id }`          | `{ message, ocr_text }`                                                  | `{ error }`    |
| **Create Reminder**                      | POST        | `/api/reminders`                                            | Create medicine reminder                                                                        | `{ user_id, medicine_name, time, repeat }`        | `{ message }`                                                            | `{ error }`    |
| **Create Digital Prescription (Doctor)** | POST        | `/api/doctors/prescriptions`                                | Doctor creates prescription for a patient                                                       | `{ doctor_id, user_id, medicines[] }`             | `{ message }`                                                            | `{ error }`    |
| **Update Inventory (Pharmacy)**          | POST        | `/api/pharmacies/inventory`                                 | Pharmacy updates stock details                                                                  | `{ pharmacy_id, medicines[] }`                    | `{ message }`                                                            | `{ error }`    |


| API                                                 | Purpose                                                            | Endpoint Usage                                                                                              |
| --------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Google Maps Places API**                          | Locate pharmacies within a radius based on customer’s GPS location | Used in `/api/medicines/search` to append `lat` and `lng` parameters, returning sorted results by distance. |
| **Google Maps Distance Matrix API**                 | Calculate distance between customer and pharmacy                   | Enriches search results with `distance_km`.                                                                 |
| **OCR API (e.g., Google Cloud Vision / Tesseract)** | Extract medicine names & dosage from prescription image            | Used in `/api/prescriptions/upload` to process `file` input and return `ocr_text`.                          |


