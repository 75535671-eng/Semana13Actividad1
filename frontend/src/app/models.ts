export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
}

export interface TaskCreate {
  title: string;
  description: string;
  completed?: boolean;
}

export interface Message {
  id: string;
  user: string;
  text: string;
  timestamp?: number;
}

export interface MessageCreate {
  user: string;
  text: string;
}
