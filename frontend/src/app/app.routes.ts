import { Routes } from '@angular/router';
import { FirestoreComponent } from './components/firestore/firestore.component';
import { RealtimeComponent } from './components/realtime/realtime.component';

export const routes: Routes = [
  { path: '', redirectTo: 'firestore', pathMatch: 'full' },
  { path: 'firestore', component: FirestoreComponent },
  { path: 'realtime', component: RealtimeComponent },
];
