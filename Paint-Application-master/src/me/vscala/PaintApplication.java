package me.vscala;

import me.vscala.Listeners.KeyboardInput;
import me.vscala.Listeners.MouseInput;
import me.vscala.Tools.ToolAction;
import me.vscala.Tools.ToolManager;

import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.awt.image.BufferStrategy;
import java.util.ArrayList;

public class PaintApplication extends JFrame implements Runnable {
    private final BufferStrategy bs;
    private volatile boolean running;
    private final Thread paintThread;
    private final MouseInput mouse;
    private final KeyboardInput keyboard;
    private final ToolManager toolManager;
    //private final ArrayList<Point> lines = new ArrayList<>();
    private final ArrayList<ToolAction> actions = new ArrayList<>();
    private boolean drawingLine;
    private int colorIndex;
    private final Canvas canvas = new Canvas();

    private final Color[] COLORS = {
            Color.RED,
            Color.GREEN,
            Color.YELLOW,
            Color.BLUE
    };


    public PaintApplication() {
        // Initializing tool manage
        toolManager = new ToolManager();

        // Initializing canvas
        setupCanvas();
        bs = canvas.getBufferStrategy();

        // Initializing Listeners
        mouse = new MouseInput();
        keyboard = new KeyboardInput();
        setupListeners();

        // Initializing paint thread
        paintThread = new Thread(this);
        paintThread.start();

    }

    private void setupCanvas() {
        canvas.setSize(640, 480);
        canvas.setBackground(Color.BLACK);
        canvas.setIgnoreRepaint(true);
        getContentPane().add(canvas);
        setTitle("Paint Application");
        setIgnoreRepaint(true);
        pack();
        setVisible(true);
        canvas.createBufferStrategy(2);
        canvas.requestFocus();
    }

    private void setupListeners() {
        canvas.addKeyListener(keyboard);
        canvas.addMouseListener(mouse);
        canvas.addMouseMotionListener(mouse);
        canvas.addMouseWheelListener(mouse);
    }

    public void run() {
        running = true;
        while(running) {
            processInput();
            renderFrame();
            sleep(10L);
        }
    }

    private void renderFrame() {
        do {
            do {
                Graphics g = null;
                try {
                    g = bs.getDrawGraphics();
                    g.clearRect(0, 0, getWidth(), getHeight());
                    render(g);
                } finally {
                    if(g != null) {
                        g.dispose();
                    }
                }
            } while(bs.contentsRestored());
            bs.show();
        } while(bs.contentsLost());
    }

    private void sleep(long sleep) {
        try {
            Thread.sleep(sleep);
        } catch(InterruptedException ex) {
            ex.printStackTrace();
        }
    }

    private void processInput() {
        keyboard.poll();
        mouse.poll();
        if(keyboard.keyDownOnce(KeyEvent.VK_SPACE)) {
            System.out.println("VK_SPACE");
        }
        if(keyboard.keyDownOnce(KeyEvent.VK_LEFT)) {
            toolManager.selectNextTool();
            System.out.println("VK_LEFT" + toolManager.getSelectedTool());

        }
        Color color = COLORS[ Math.abs(colorIndex % COLORS.length) ];
        switch (toolManager.getSelectedTool()) {
            case 0:
                if(mouse.buttonDownOnce(MouseEvent.BUTTON1)) {
                    drawingLine = true;
                }
                if(mouse.buttonDown(MouseEvent.BUTTON1)) {
                    ToolAction toolAction = new ToolAction(0, mouse.getPosition(), color);
                    actions.add(toolAction);
                } else if(drawingLine) {
                    ToolAction toolAction = new ToolAction(0, null, color);
                    actions.add(toolAction);
                    drawingLine = false;
                }
                break;
            case 1:
                if (mouse.buttonDownOnce(MouseEvent.BUTTON1) || mouse.buttonDown(MouseEvent.BUTTON1)) {
                    ToolAction toolAction = new ToolAction(1, mouse.getPosition(), color);
                    actions.add(toolAction);
                }

        }
        if(keyboard.keyDownOnce(KeyEvent.VK_C)) {
            actions.clear();
        }
    }

    private void render(Graphics g) {
        colorIndex += mouse.getNotches();
        g.drawString("Use mouse to draw lines", 30, 45);
        g.drawString("Press C to clear lines", 30, 60);
        g.drawString("Mouse Wheel cycles colors", 30, 75);
        g.drawString(mouse.getPosition().toString(), 30, 90);
        for(int i = 0; i < actions.size() - 1; ++i) {
            //System.out.print(actions.get(i).getPoint().toString());
            g.setColor(actions.get(i).getColor());
            switch (actions.get(i).getAction()) {
                case 0:
                    if (i >= actions.size() - 2) break;
                    //if (actions.get(i+1).getAction() != 0) break;
                    Point p1 = actions.get(i).getPoint();
                    Point p2 = actions.get(i+1).getPoint();
                    if(!(p1 == null || p2 == null))
                        g.drawLine(p1.x, p1.y, p2.x, p2.y);
                    break;
                case 1:
                    for (int j = 0; j < getHeight()-1; j++)
                        g.drawLine(0, j, getWidth(), j);
            }
        }
    }

    protected void onWindowClosing() {
        try {
            running = false;
            paintThread.join();
        } catch(InterruptedException e) {
            e.printStackTrace();
        }
        System.exit(0);
    }
}
