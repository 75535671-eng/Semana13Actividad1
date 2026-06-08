import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { FirebaseService } from '../../services/firebase.service';
import { Task } from '../../models';

@Component({
  selector: 'app-firestore',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './firestore.component.html',
  styleUrl: './firestore.component.scss',
})
export class FirestoreComponent implements OnInit, OnDestroy {
  private readonly firebase = inject(FirebaseService);
  private tasksSub?: Subscription;

  tasks: Task[] = [];
  loading = true;
  error = '';

  newTitle = '';
  newDescription = '';

  ngOnInit(): void {
    this.tasksSub = this.firebase.getTasksRealtime().subscribe({
      next: (tasks) => {
        this.tasks = tasks;
        this.loading = false;
        this.error = '';
      },
      error: () => {
        this.error =
          'Error al conectar con Firestore. Verifica las reglas de seguridad en Firebase Console.';
        this.loading = false;
      },
    });
  }

  ngOnDestroy(): void {
    this.tasksSub?.unsubscribe();
  }

  async addTask(): Promise<void> {
    if (!this.newTitle.trim()) return;

    try {
      await this.firebase.addTaskDirect({
        title: this.newTitle.trim(),
        description: this.newDescription.trim(),
        completed: false,
      });
      this.newTitle = '';
      this.newDescription = '';
      this.error = '';
    } catch {
      this.error = 'Error al crear la tarea en Firestore.';
    }
  }

  async toggleTask(task: Task): Promise<void> {
    try {
      await this.firebase.updateTaskDirect(task.id, { completed: !task.completed });
      this.error = '';
    } catch {
      this.error = 'Error al actualizar la tarea.';
    }
  }

  async deleteTask(id: string): Promise<void> {
    try {
      await this.firebase.deleteTaskDirect(id);
      this.error = '';
    } catch {
      this.error = 'Error al eliminar la tarea.';
    }
  }
}
