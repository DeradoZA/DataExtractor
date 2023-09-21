import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-match',
  templateUrl: './match.component.html',
  styleUrls: ['./match.component.css']
})
export class MatchComponent {
  url: string = 'http://127.0.0.1:5000/api/randomMatch';
  match_prediction: number = 0;
  team1_avg_stats: number[] = []
  team2_avg_stats: number[] = []
  team1_player_stats: number[] = []
  team2_player_stats: number[] = []

  constructor(private http: HttpClient) {}

  handleClick() {
    this.http.get<any>(this.url).subscribe(
      (data) => {
        this.match_prediction = data['match_prediction']
        this.team1_avg_stats = data['team1_avg_stats']
        this.team2_avg_stats = data['team2_avg_stats']
        this.team1_player_stats = data['team1_player_stats']
        this.team2_player_stats = data['team2_player_stats']
        console.log(data);
      },
      (error) => {
        console.log('API Error --> ', error);
      }
    );
  }
}