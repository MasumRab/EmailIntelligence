import express, { type Application } from 'express';
import { vi } from 'vitest';
import request from 'supertest';
import { z } from 'zod';
import emailRoutes from './emailRoutes';
import { pythonNLP } from './python-bridge';

vi.mock('./python-bridge', () => ({
  pythonNLP: {
    getEmails: vi.fn(),
    getEmailById: vi.fn(),
    createEmail: vi.fn(),
    updateEmail: vi.fn(),
  },
}));

vi.mock('@shared/schema', () => ({
  insertEmailSchema: {
    parse: (data: any) => {
      if (!data.subject) {
        throw new z.ZodError([]);
      }
      return data;
    },
  },
}));

const app: Application = express();
app.use(express.json());
app.use('/api/emails', emailRoutes);

describe('Email Routes', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('GET /api/emails', () => {
    it('should get all emails and return 200', async () => {
      const mockEmails = [{ id: 1, subject: 'Test Email' }];
      (pythonNLP.getEmails as ReturnType<typeof vi.fn>).mockResolvedValue(mockEmails);

      const response = await request(app).get('/api/emails');

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockEmails);
    });

    it('should search emails if "search" query is present and return 200', async () => {
      const mockEmails = [{ id: 1, subject: 'Searched Email' }];
      const searchQuery = 'test_search';
      (pythonNLP.getEmails as ReturnType<typeof vi.fn>).mockResolvedValue(mockEmails);

      const response = await request(app).get(`/api/emails?search=${searchQuery}`);

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockEmails);
      expect(pythonNLP.getEmails).toHaveBeenCalledWith(undefined, searchQuery);
    });

    it('should get emails by category if "category" query is present and return 200', async () => {
        const mockEmails = [{ id: 1, subject: 'Category Email', categoryId: 1 }];
        const categoryId = '1';
        (pythonNLP.getEmails as ReturnType<typeof vi.fn>).mockResolvedValue(mockEmails);

        const response = await request(app).get(`/api/emails?category=${categoryId}`);

        expect(response.status).toBe(200);
        expect(response.body).toEqual(mockEmails);
        expect(pythonNLP.getEmails).toHaveBeenCalledWith(categoryId, undefined);
      });

    it('should return 500 if fetching emails fails', async () => {
      (pythonNLP.getEmails as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('API Error'));

      const response = await request(app).get('/api/emails');

      expect(response.status).toBe(500);
      expect(response.body).toEqual({ message: 'Failed to fetch emails' });
    });
  });

  describe('GET /api/emails/:id', () => {
    it('should get an email by ID and return 200', async () => {
      const mockEmail = { id: 1, subject: 'Test Email' };
      (pythonNLP.getEmailById as ReturnType<typeof vi.fn>).mockResolvedValue(mockEmail);

      const response = await request(app).get('/api/emails/1');

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockEmail);
    });

    it('should return 404 if email not found', async () => {
      (pythonNLP.getEmailById as ReturnType<typeof vi.fn>).mockResolvedValue(null);

      const response = await request(app).get('/api/emails/99');

      expect(response.status).toBe(404);
      expect(response.body).toEqual({ message: 'Email not found' });
    });
  });

  describe('POST /api/emails', () => {
    it('should create an email and return 201', async () => {
      const newEmailData = { subject: 'New Email', content: 'Content', sender: 't@t.com', senderEmail: 't@t.com', time:'t', preview:'p' };
      const createdEmail = { id: 2, ...newEmailData };
      (pythonNLP.createEmail as ReturnType<typeof vi.fn>).mockResolvedValue(createdEmail);

      const response = await request(app).post('/api/emails').send(newEmailData);

      expect(response.status).toBe(201);
      expect(response.body).toEqual(createdEmail);
    });

    it('should return 400 for invalid email data', async () => {
      const invalidEmailData = { content: 'some content' };
      const response = await request(app).post('/api/emails').send(invalidEmailData);
      expect(response.status).toBe(400);
    });
  });

  describe('PUT /api/emails/:id', () => {
    it('should update an email and return 200', async () => {
      const updateData = { subject: 'Updated Subject' };
      const updatedEmail = { id: 1, subject: 'Updated Subject' };
      (pythonNLP.updateEmail as ReturnType<typeof vi.fn>).mockResolvedValue(updatedEmail);

      const response = await request(app).put('/api/emails/1').send(updateData);

      expect(response.status).toBe(200);
      expect(response.body).toEqual(updatedEmail);
    });

    it('should return 404 if email to update not found', async () => {
      (pythonNLP.updateEmail as ReturnType<typeof vi.fn>).mockResolvedValue(null);

      const response = await request(app).put('/api/emails/99').send({ subject: 'test' });

      expect(response.status).toBe(404);
      expect(response.body).toEqual({ message: 'Email not found' });
    });
  });
});
