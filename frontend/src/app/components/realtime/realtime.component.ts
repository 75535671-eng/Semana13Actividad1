import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { FirebaseService } from '../../services/firebase.service';
import { Message } from '../../models';

@Component({
  selector: 'app-realtime',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './realtime.component.html',
  styleUrl: './realtime.component.scss',
})
export class RealtimeComponent implements OnInit, OnDestroy {
  private readonly firebase = inject(FirebaseService);
  private messagesSub?: Subscription;

  messages: Message[] = [];
  loading = true;
  error = '';

  newUser = '';
  newText = '';

  ngOnInit(): void {
    this.messagesSub = this.firebase.getMessagesRealtime().subscribe({
      next: (messages) => {
        this.messages = messages;
        this.loading = false;
        this.error = '';
      },
      error: () => {
        this.error =
          'Error al conectar con Realtime Database. Actívala en Firebase Console > Realtime Database.';
        this.loading = false;
      },
    });
  }

  ngOnDestroy(): void {
    this.messagesSub?.unsubscribe();
  }

  async sendMessage(): Promise<void> {
    if (!this.newUser.trim() || !this.newText.trim()) return;

    try {
      await this.firebase.addMessageDirect({
        user: this.newUser.trim(),
        text: this.newText.trim(),
      });
      this.newText = '';
      this.error = '';
    } catch {
      this.error = 'Error al enviar el mensaje.';
    }
  }

  async deleteMessage(id: string): Promise<void> {
    try {
      await this.firebase.deleteMessageDirect(id);
      this.error = '';
    } catch {
      this.error = 'Error al eliminar el mensaje.';
    }
  }

  formatTime(timestamp?: number): string {
    if (!timestamp) return '';
    return new Date(timestamp * 1000).toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
    });
  }
}
