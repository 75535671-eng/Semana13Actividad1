import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Message, MessageCreate, Task, TaskCreate } from '../models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = environment.apiUrl;

  // --- Firestore (vía API FastAPI) ---
  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.baseUrl}/api/firestore/tasks`);
  }

  createTask(task: TaskCreate): Observable<Task> {
    return this.http.post<Task>(`${this.baseUrl}/api/firestore/tasks`, task);
  }

  updateTask(id: string, data: Partial<Task>): Observable<Task> {
    return this.http.put<Task>(`${this.baseUrl}/api/firestore/tasks/${id}`, data);
  }

  deleteTask(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/api/firestore/tasks/${id}`);
  }

  // --- Realtime Database (vía API FastAPI) ---
  getMessages(): Observable<Message[]> {
    return this.http.get<Message[]>(`${this.baseUrl}/api/realtime/messages`);
  }

  createMessage(message: MessageCreate): Observable<Message> {
    return this.http.post<Message>(`${this.baseUrl}/api/realtime/messages`, message);
  }

  deleteMessage(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/api/realtime/messages/${id}`);
  }
}
