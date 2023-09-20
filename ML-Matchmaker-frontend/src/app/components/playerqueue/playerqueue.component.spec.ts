import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerqueueComponent } from './playerqueue.component';

describe('PlayerqueueComponent', () => {
  let component: PlayerqueueComponent;
  let fixture: ComponentFixture<PlayerqueueComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PlayerqueueComponent]
    });
    fixture = TestBed.createComponent(PlayerqueueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
