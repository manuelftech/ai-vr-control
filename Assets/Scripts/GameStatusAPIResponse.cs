using System;
using System.Collections.Generic;

[Serializable]
public class GameStatusAPIResponse
{
    public List<GameObjectStatus> gameObjects;
}

[Serializable]
public class GameObjectStatus
{
    public string instanceId { get; set; }
    public string tag { get; set; } // cube
    public float color { get; set; }
    public int constantForce { get; set; } // 9.83
    public int x { get; set; }
    public int y { get; set; }
    public int z { get; set; }
}