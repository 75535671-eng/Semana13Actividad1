import { Injectable, inject } from '@angular/core';
import {
  Firestore,
  collection,
  collectionData,
  addDoc,
  deleteDoc,
  doc,
  updateDoc,
  serverTimestamp,
} from '@angular/fire/firestore';
import {
  Database,
  ref,
  list,
  push,
  remove,
} from '@angular/fire/database';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Message, Task } from '../models';

@Injectable({ providedIn: 'root' })
export class FirebaseService {
  private readonly firestore = inject(Firestore);
  private readonly database = inject(Database);

  getTasksRealtime(): Observable<Task[]> {
    const tasksRef = collection(this.firestore, 'tasks');
    return collectionData(tasksRef, { idField: 'id' }).pipe(
      map((tasks) =>
        (tasks as Task[]).sort((a, b) => a.title.localeCompare(b.title))
      )
    );
  }

  async addTaskDirect(task: Omit<Task, 'id'>): Promise<void> {
    await addDoc(collection(this.firestore, 'tasks'), {
      ...task,
      createdAt: serverTimestamp(),
    });
  }

  async updateTaskDirect(id: string, data: Partial<Task>): Promise<void> {
    await updateDoc(doc(this.firestore, 'tasks', id), data);
  }

  async deleteTaskDirect(id: string): Promise<void> {
    await deleteDoc(doc(this.firestore, 'tasks', id));
  }

  getMessagesRealtime(): Observable<Message[]> {
    const messagesRef = ref(this.database, 'messages');
    return list(messagesRef).pipe(
      map((changes) => {
        const messages = changes.map((c) => ({
          id: c.snapshot.key!,
          ...(c.snapshot.val() as Omit<Message, 'id'>),
        }));
        return messages.sort((a, b) => (b.timestamp ?? 0) - (a.timestamp ?? 0));
      })
    );
  }

  async addMessageDirect(message: { user: string; text: string }): Promise<void> {
    const messagesRef = ref(this.database, 'messages');
    await push(messagesRef, {
      ...message,
      timestamp: Date.now() / 1000,
    });
  }

  async deleteMessageDirect(id: string): Promise<void> {
    await remove(ref(this.database, `messages/${id}`));
  }
}
