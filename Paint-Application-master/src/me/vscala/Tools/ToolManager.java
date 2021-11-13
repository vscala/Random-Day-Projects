package me.vscala.Tools;

public class ToolManager {
    private int selectedTool;
    private final int TOOL_COUNT = 2;
    private Tool[] tools;

    public ToolManager() {
        selectedTool = 1;
        tools = new Tool[TOOL_COUNT];
        tools[0] = new BrushTool();
        tools[1] = new PaintBucketTool();
    }

    public int getSelectedTool() {
        return selectedTool;
    }

    public void switchTool(int index) {
        selectedTool = index;
    }

    public void selectNextTool() {
        selectedTool = (selectedTool + 1) % TOOL_COUNT;
    }
}
