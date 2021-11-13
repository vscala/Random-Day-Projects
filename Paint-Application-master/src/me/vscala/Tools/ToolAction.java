package me.vscala.Tools;

import java.awt.*;

public class ToolAction {
    int action;
    Point point;
    Color color;
    public ToolAction(int action, Point point, Color color) {
        this.action = action;
        this.point = point;
        this.color = color;
    }
    public int getAction() { return action; }
    public Point getPoint() { return point; }
    public Color getColor() { return color; }
}
