package me.vscala.Listeners;

import java.awt.*;
import java.awt.event.*;

public class MouseInput implements MouseListener, MouseMotionListener, MouseWheelListener {
    private static final int BUTTON_COUNT = 3;

    private Point mousePos;
    private Point currentPos;
    private final boolean[] mouse;
    private final int[] polled;
    private int notches;
    private int polledNotches;

    public MouseInput() {
        mousePos = new Point(0, 0);
        currentPos = new Point(0, 0);
        mouse = new boolean[BUTTON_COUNT];
        polled = new int[BUTTON_COUNT];
    }

    public synchronized void poll() {
        mousePos = new Point(currentPos);
        polledNotches = notches;
        notches = 0;

        for (int i = 0; i < mouse.length; ++i) {
            if (mouse[i]) {
                polled[i]++;
            } else {
                polled[i] = 0;
            }
        }
    }

    public Point getPosition() {
        return mousePos;
    }

    public int getNotches() {
        return polledNotches;
    }

    public boolean buttonDown(int button) {
        return polled[button-1] >= 1;
    }

    public boolean buttonDownOnce(int button) {
        return polled[button-1] == 1;
    }


    @Override
    public void mouseClicked(MouseEvent e) { }

    @Override
    public void mousePressed(MouseEvent e) {
        int button = e.getButton() - 1;
        if (button >= 0 && button < mouse.length) {
            mouse[button] = true;
        }
    }

    @Override
    public void mouseReleased(MouseEvent e) {
        int button = e.getButton() - 1;
        if (button >= 0 && button < mouse.length) {
            mouse[button] = false;
        }
    }

    @Override
    public void mouseEntered(MouseEvent e) {
        mouseMoved(e);
    }

    @Override
    public void mouseExited(MouseEvent e) {
        mouseMoved(e);
    }

    @Override
    public void mouseDragged(MouseEvent e) {
        mouseMoved(e);
    }

    @Override
    public void mouseMoved(MouseEvent e) {
        currentPos = e.getPoint();
    }

    @Override
    public void mouseWheelMoved(MouseWheelEvent e) {
        notches += e.getWheelRotation();
    }
}
