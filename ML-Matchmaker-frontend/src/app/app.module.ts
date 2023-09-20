import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {HttpClientModule} from '@angular/common/http'

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ButtonComponent } from './components/button/button.component';
import { PlayerqueueComponent } from './components/playerqueue/playerqueue.component';
import { PlayerboxComponent } from './components/playerbox/playerbox.component';
import { MatchComponent } from './components/match/match.component';


@NgModule({
  declarations: [
    AppComponent,
    ButtonComponent,
    PlayerqueueComponent,
    PlayerboxComponent,
    MatchComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FontAwesomeModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
