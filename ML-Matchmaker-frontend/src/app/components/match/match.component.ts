import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-match',
  templateUrl: './match.component.html',
  styleUrls: ['./match.component.css']
})
export class MatchComponent {
  urlRandomMatch: string = 'http://127.0.0.1:5000/api/randomMatch';
  urlCustomMatch: string = 'http://127.0.0.1:5000/api/customMatch';
  match_prediction: number = 0;
  team1_avg_stats: number[] = []
  team2_avg_stats: number[] = []
  team1_player_stats: number[] = []
  team2_player_stats: number[] = []
  dataFromFeatureFormA: any;
  dataFromFeatureFormB: any;

  constructor(private http: HttpClient) {}

  handleClick() {
    this.http.post<any>(this.urlCustomMatch, {teamA: this.dataFromFeatureFormA, teamB: this.dataFromFeatureFormB})
    .subscribe((response) => {
      this.match_prediction = response['match_prediction']
      this.match_prediction = this.match_prediction * 100;
      this.match_prediction = Math.round(this.match_prediction)
    }, (error) => {
      console.error('Error: ', error)
    });

    console.log(this.dataFromFeatureFormA)
  }

  handleDataFormA(data: any)
  {
    this.dataFromFeatureFormA = data;
  }

  handleDataFormB(data: any)
  {
    this.dataFromFeatureFormB = data;
  }
}