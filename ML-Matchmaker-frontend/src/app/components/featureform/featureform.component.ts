import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-featureform',
  templateUrl: './featureform.component.html',
  styleUrls: ['./featureform.component.css']
})
export class FeatureformComponent {
  @Input() teamDescriptor!: string;
  teamELO: string= "";
  teamRWS: string= "";
  teamRating: string= "";
  teamRating2: string= "";
  teamKR: string= "";
  teamKD: string= "";
  teamKAST: string= "";
  teamADR: string= "";

  @Output() featureFormData: EventEmitter<any> = new EventEmitter<any>();

  sendDataToMatch()
  {
    const formData = {
      teamELO: this.teamELO,
      teamRWS: this.teamRWS,
      teamRating: this.teamRating,
      teamRating2: this.teamRating2,
      teamKR: this.teamKR,
      teamKD: this.teamKD,
      teamKAST: this.teamKAST,
      teamADR: this.teamADR
    }

    this.featureFormData.emit(formData);
  }
}
