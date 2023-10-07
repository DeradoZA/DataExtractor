import { Component, Output, EventEmitter, Input } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.css']
})
export class ButtonComponent {
    @Output() customClick = new EventEmitter<void>();
    @Input() buttonLabel! : string;

    emitCustomEvent()
    {
      this.customClick.emit();
    }
}
