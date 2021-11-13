package me.vscala;

import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

public class Main {

    public static void main(String[] args) {
        final PaintApplication paintApplication = new PaintApplication();
        paintApplication.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e ) {
                paintApplication.onWindowClosing();
            }
        });
    }
}
