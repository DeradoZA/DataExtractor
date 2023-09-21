import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-playerqueue',
  templateUrl: './playerqueue.component.html',
  styleUrls: ['./playerqueue.component.css']
})
export class PlayerqueueComponent {
    @Input() teamStats: number[] = [];
    @Input() playerTeamStats: number[] = [];
}
