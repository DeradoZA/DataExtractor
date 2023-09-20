import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerboxComponent } from './playerbox.component';

describe('PlayerboxComponent', () => {
  let component: PlayerboxComponent;
  let fixture: ComponentFixture<PlayerboxComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PlayerboxComponent]
    });
    fixture = TestBed.createComponent(PlayerboxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
