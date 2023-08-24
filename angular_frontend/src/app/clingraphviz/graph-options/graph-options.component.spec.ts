import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphOptionsComponent } from './graph-options.component';

describe('GraphOptionsComponent', () => {
  let component: GraphOptionsComponent;
  let fixture: ComponentFixture<GraphOptionsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [GraphOptionsComponent]
    });
    fixture = TestBed.createComponent(GraphOptionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
