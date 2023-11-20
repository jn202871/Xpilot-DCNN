#include <Python.h>
#include "xpilot_ai.h"


static PyObject *
xpai_setargs(PyObject *self, PyObject *args)
{
    char *command;
    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    AI_xpilot_setargs(command);
    return Py_BuildValue("i", 1);
}
static PyObject *
xpai_launch(PyObject *self, PyObject *args)
{
	AI_xpilot_launch ();
    return Py_BuildValue("i", 0);
}



static PyObject *
xpai_AIself_name(PyObject *self, PyObject *args)
{
	return Py_BuildValue("s", AIself_name());	
}
static PyObject *
xpai_AIself_alive(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_alive());	
}
static PyObject *
xpai_AIself_id(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_id());	
}
static PyObject *
xpai_AIself_heading(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_heading());	
}
static PyObject *
xpai_AIself_vel(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_vel());	
}
static PyObject *
xpai_AIself_track(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_track());	
}
static PyObject *
xpai_AIself_mapx(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_mapx());	
}
static PyObject *
xpai_AIself_mapy(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_mapy());	
}

static PyObject *
xpai_AIself_x(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_x());	
}
static PyObject *
xpai_AIself_y(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_y());	
}
static PyObject *
xpai_AIself_team(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_team());	
}
static PyObject *
xpai_AIself_life(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_life());	
}
static PyObject *
xpai_AIself_shield(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_shield());	
}
static PyObject *
xpai_AIself_reload(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AIself_reload());	
}

static PyObject *
xpai_AIself_score(PyObject *self, PyObject *args)
{
	return Py_BuildValue("f", AIself_score());	
}
static PyObject *
xpai_AI_teamplay(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", AI_teamplay());	
}
static PyObject *
xpai_AIself_destruct(PyObject *self, PyObject *args)
{
	AIself_destruct();
    Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
xpai_AIself_thrust(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	AIself_thrust(val);	
    Py_INCREF(Py_None);
	return Py_None;
}
static PyObject *
xpai_AIself_turn(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	AIself_turn(val);	
    Py_INCREF(Py_None);
	return Py_None;
}
static PyObject *
xpai_AIself_shoot(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	AIself_shoot(val);	
    Py_INCREF(Py_None);
	return Py_None;
}
static PyObject *
xpai_AIself_shield_enable(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	AIself_shield_enable(val);	
    Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
xpai_setmaxturn(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	AI_setmaxturn(val);	
    Py_INCREF(Py_None);
	return Py_None;
}
static PyObject *
xpai_AI_presskey(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	AI_presskey(val);	
    Py_INCREF(Py_None);
	return Py_None;
}
static PyObject *
xpai_AI_releasekey(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	AI_releasekey(val);	
    Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
xpai_AI_talk(PyObject *self, PyObject *args)
{
	char* val;
	PyArg_ParseTuple(args, "s", &val);	
	AI_talk(val);
    Py_INCREF(Py_None);
	return Py_None;	
}

static PyObject *
xpai_AImsg_body(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("s", AImsg_body(val));	
}
static PyObject *
xpai_AImsg_from(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("s", AImsg_from(val));	
}
static PyObject *
xpai_AImsg_to(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("s", AImsg_to(val));	
}

static PyObject *
xpai_AIself_HUD_name(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("s", AIself_HUD_name(val));	
}
static PyObject *
xpai_AIself_HUD_score(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("f", AIself_HUD_score(val));	
}
static PyObject *
xpai_AIself_HUD_time(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIself_HUD_time(val));	
}

static PyObject *
xpai_AIship_x(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_x(val));	
}
static PyObject *
xpai_AIship_y(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_y(val));	
}
static PyObject *
xpai_AIship_heading(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_heading(val));	
}
static PyObject *
xpai_AIship_vel(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_vel(val));	
}
static PyObject *
xpai_AIship_acc(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_acc(val));	
}
static PyObject *
xpai_AIship_track(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_track(val));	
}
static PyObject *
xpai_AIship_dist(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_dist(val));	
}
static PyObject *
xpai_AIship_id(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_id(val));	
}
static PyObject *
xpai_AIship_xdir(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_xdir(val));	
}
static PyObject *
xpai_AIship_shield(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_shield(val));	
}
static PyObject *
xpai_AIship_life(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_life(val));	
}
static PyObject *
xpai_AIship_team(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_team(val));	
}
static PyObject *
xpai_AIship_reload(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_reload(val));	
}
static PyObject *
xpai_AIship_aimdir(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIship_aimdir(val));	
}
static PyObject *
xpai_AIship_name(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("s", AIship_name(val));	
}

static PyObject *
xpai_AIshot_x(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_x(val));	
}
static PyObject *
xpai_AIshot_y(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_y(val));	
}
static PyObject *
xpai_AIshot_dist(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_dist(val));	
}
static PyObject *
xpai_AIshot_xdir(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_xdir(val));	
}
static PyObject *
xpai_AIshot_vel(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_vel(val));	
}
static PyObject *
xpai_AIshot_track(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_track(val));	
}
static PyObject *
xpai_AIshot_imaginary(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_imaginary(val));	
}
static PyObject *
xpai_AIshot_idir(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_idir(val));	
}
static PyObject *
xpai_AIshot_idist(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_idist(val));	
}
static PyObject *
xpai_AIshot_itime(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_itime(val));	
}
static PyObject *
xpai_AIshot_alert(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_alert(val));	
}
static PyObject *
xpai_AIshot_id(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIshot_id(val));	
}

static PyObject *
xpai_AIradar_x(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIradar_x(val));	
}
static PyObject *
xpai_AIradar_y(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIradar_y(val));	
}
static PyObject *
xpai_AIradar_dist(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIradar_dist(val));	
}
static PyObject *
xpai_AIradar_xdir(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIradar_xdir(val));	
}
static PyObject *
xpai_AIradar_enemy(PyObject *self, PyObject *args)
{
	int val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("i", AIradar_enemy(val));	
}


static PyObject *
xpai_anglediff(PyObject *self, PyObject *args)
{
	int val0, val1;
	PyArg_ParseTuple(args, "ii", &val0, &val1);	
	return Py_BuildValue("i", anglediff(val0, val1));	
}
static PyObject *
xpai_angleadd(PyObject *self, PyObject *args)
{
	int val0, val1;
	PyArg_ParseTuple(args, "ii", &val0, &val1);	
	return Py_BuildValue("i", angleadd(val0, val1));	
}

static PyObject *
xpai_rad(PyObject *self, PyObject *args)
{
	double val;
	PyArg_ParseTuple(args, "i", &val);	
	return Py_BuildValue("d", rad(val));	
}
static PyObject *
xpai_deg(PyObject *self, PyObject *args)
{
	double val;
	PyArg_ParseTuple(args, "d", &val);
	return Py_BuildValue("i", deg(val));
}
static PyObject *
xpai_wallbetween(PyObject *self, PyObject *args)
{
  int val0, val1, val2, val3;
  PyArg_ParseTuple(args, "iiii", &val0, &val1, &val2, &val3);
  return Py_BuildValue("i", AI_wallbetween(val0, val1, val2, val3));
}
static PyObject *
xpai_wallbetween_x(PyObject *self, PyObject *args)
{
  int val0, val1, val2, val3;
  PyArg_ParseTuple(args, "iiii", &val0, &val1, &val2, &val3);
  return Py_BuildValue("i", AI_wallbetween_x(val0, val1, val2, val3));
}
static PyObject *
xpai_wallbetween_y(PyObject *self, PyObject *args)
{
  int val0, val1, val2, val3;
  PyArg_ParseTuple(args, "iiii", &val0, &val1, &val2, &val3);
  return Py_BuildValue("i", AI_wallbetween_y(val0, val1, val2, val3));
}
static PyObject *
xpai_map_get(PyObject *self, PyObject *args)
{
  int val0, val1;
  PyArg_ParseTuple(args, "ii", &val0, &val1);
  return Py_BuildValue("i", AImap_get(val0, val1));
}
static PyObject *
xpai_map_set(PyObject *self, PyObject *args)
{
  int val0, val1, val2;
  PyArg_ParseTuple(args, "iii", &val0, &val1, &val2);
  AImap_set(val0, val1, val2);
   Py_INCREF(Py_None);
	return Py_None;
}
static PyObject *
xpai_tomap(PyObject *self, PyObject *args)
{
  int val;
  PyArg_ParseTuple(args, "i", &val);
  return Py_BuildValue("i", tomap(val));
}
static PyObject *
xpai_frmap(PyObject *self, PyObject *args)
{
  int val;
  PyArg_ParseTuple(args, "i", &val);
  return Py_BuildValue("i", frmap(val));
}
static PyObject *AImain_callback = NULL;

static PyObject *
xpai_set_AImain(PyObject *dummy, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O", &temp)) {
        if (!PyCallable_Check(temp)) {
			printf("BIG ERROR\n");
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);         /* Add a reference to new callback */
        Py_XDECREF(AImain_callback);  /* Dispose of previous callback */
        AImain_callback = temp;       /* Remember new callback */
        /* Boilerplate to return "None" */
        Py_INCREF(Py_None);
        result = Py_None;
    }
    return result;
}

static PyObject *
xpai_call_AImain(PyObject *self, PyObject *args)
{
	PyObject *arglist = Py_BuildValue("");
	
	if (AImain_callback == NULL)
		printf("It's NULL\n");
	else {
		printf("working %x\n", (unsigned int)AImain_callback);
		PyEval_CallObject(AImain_callback, arglist);
	}
    Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef xpaiMethods[] = 
{
    { "setargs", xpai_setargs, METH_VARARGS, 
      "setargs(string)->int"},
    { "launch", xpai_launch, METH_VARARGS, 
      "launch()->int"},

    { "self_alive", xpai_AIself_alive, METH_VARARGS,
      "self_alive()->int"},

    { "self_id", xpai_AIself_id, METH_VARARGS,
      "self_id()->int"},
    
    { "self_heading", xpai_AIself_heading, METH_VARARGS,
      "self_heading()->int"},

    { "self_vel", xpai_AIself_vel, METH_VARARGS,
      "self_vel()->int"},

    { "self_track", xpai_AIself_track, METH_VARARGS,
      "self_track()->int"},

    { "self_team", xpai_AIself_team, METH_VARARGS,
      "self_team()->int"},

    { "self_life", xpai_AIself_life, METH_VARARGS,
      "self_life()->int"},

    { "self_shield", xpai_AIself_shield, METH_VARARGS,
      "self_shield()->int"},

    { "self_reload", xpai_AIself_reload, METH_VARARGS,
      "self_reload()->int"},

    { "self_score", xpai_AIself_score, METH_VARARGS,
      "self_score()->double"},

    { "self_name", xpai_AIself_name, METH_VARARGS,
      "self_name()->string"},

    { "self_x", xpai_AIself_x, METH_VARARGS, 
      "self_x()->int"},
    { "self_y", xpai_AIself_y, METH_VARARGS, 
      "self_y()->int"},

    { "self_mapx", xpai_AIself_mapx, METH_VARARGS, 
      "self_mapx()->int"},
    { "self_mapy", xpai_AIself_mapy, METH_VARARGS, 
      "self_mapy()->int"},

    


    { "self_thrust", xpai_AIself_thrust, METH_VARARGS, 
      "self_thrust(int)->null"},
    { "self_turn", xpai_AIself_turn, METH_VARARGS, 
      "self_turn(int)->null"},
    { "self_shoot", xpai_AIself_shoot, METH_VARARGS, 
      "self_shoot(int)->null"},
    { "self_shield_enable", xpai_AIself_shield_enable, METH_VARARGS, 
      "self_shield_enable(int)->null"},
    { "setmaxturn", xpai_setmaxturn, METH_VARARGS, 
      "setmaxturn(int)->null"},
    { "self_destruct", xpai_AIself_destruct, METH_VARARGS,
      "self_destruct(int)->null"},

    
    { "self_HUD_name", xpai_AIself_HUD_name, METH_VARARGS,
      "self_HUD_name(int)->string"},
    { "self_HUD_score", xpai_AIself_HUD_score, METH_VARARGS,
      "self_HUD_score(int)->double"},
    { "self_HUD_time", xpai_AIself_HUD_time, METH_VARARGS,
      "self_HUD_time(int)->int"},

    { "ship_x", xpai_AIship_x, METH_VARARGS, 
      "ship_x(int)->int"},
    { "ship_y", xpai_AIship_y, METH_VARARGS, 
      "ship_y(int)->int"},
    { "ship_xdir", xpai_AIship_xdir, METH_VARARGS, 
      "ship_xdir(int)->int"},

    { "ship_heading", xpai_AIship_heading, METH_VARARGS,
      "ship_heading(int)->int"},
    { "ship_vel", xpai_AIship_vel, METH_VARARGS,
      "ship_vel(int)->int"}, 
    { "ship_acc", xpai_AIship_acc, METH_VARARGS,
      "ship_acc(int)->int"},
    { "ship_track", xpai_AIship_track, METH_VARARGS,
      "ship_track(int)->int"},
    { "ship_dist", xpai_AIship_dist, METH_VARARGS,
      "ship_dist(int)->int"},
    { "ship_id", xpai_AIship_id, METH_VARARGS,
      "ship_id(int)->int"},
    { "ship_shield", xpai_AIship_shield, METH_VARARGS,
      "ship_shield(int)->int"},
    { "ship_life", xpai_AIship_life, METH_VARARGS,
      "ship_life(int)->int"},
    { "ship_team", xpai_AIship_team, METH_VARARGS,
      "ship_team(int)->int"},
    { "ship_reload", xpai_AIship_reload, METH_VARARGS,
      "ship_reload(int)->int"},
    { "ship_aimdir", xpai_AIship_aimdir, METH_VARARGS,
      "ship_aimdir(int)->int"},
    { "ship_name", xpai_AIship_name, METH_VARARGS,
      "ship_name(int)->string"},

    { "shot_x", xpai_AIshot_x, METH_VARARGS,
      "shot_x(int)->int"},
    { "shot_y", xpai_AIshot_y, METH_VARARGS,
      "shot_y(int)->int"},
    { "shot_dist", xpai_AIshot_dist, METH_VARARGS,
      "shot_dist(int)->int"},
    { "shot_xdir", xpai_AIshot_xdir, METH_VARARGS,
      "shot_xdir(int)->int"},
    { "shot_vel", xpai_AIshot_vel, METH_VARARGS,
      "shot_vel(int)->int"},
    { "shot_track", xpai_AIshot_track, METH_VARARGS,
      "shot_track(int)->int"},
    { "shot_imaginary", xpai_AIshot_imaginary, METH_VARARGS,
      "shot_imaginary(int)->int"},
    { "shot_idir", xpai_AIshot_idir, METH_VARARGS,
      "shot_idir(int)->int"},
    { "shot_idist", xpai_AIshot_idist, METH_VARARGS,
      "shot_idist(int)->int"},
    { "shot_itime", xpai_AIshot_itime, METH_VARARGS,
      "shot_itime(int)->int"},
    { "shot_alert", xpai_AIshot_alert, METH_VARARGS,
      "shot_alert(int)->int"},
    { "shot_id", xpai_AIshot_id, METH_VARARGS,
      "shot_id(int)->int"},

    { "radar_x", xpai_AIradar_x, METH_VARARGS,
      "radar_x(int)->int"},
    { "radar_y", xpai_AIradar_y, METH_VARARGS,
      "radar_y(int)->int"},
    { "radar_dist", xpai_AIradar_dist, METH_VARARGS,
      "radar_dist(int)->int"},
    { "radar_xdir", xpai_AIradar_xdir, METH_VARARGS,
      "radar_xdir(int)->int"},
    { "radar_enemy", xpai_AIradar_enemy, METH_VARARGS,
      "radar_enemy(int)->int"},



    { "talk", xpai_AI_talk, METH_VARARGS, 
      "talk(string)->null"},

    { "teamplay", xpai_AI_teamplay, METH_VARARGS,
      "teamplay()->int"},

    { "presskey", xpai_AI_presskey, METH_VARARGS,
      "presskey(int)->null"},

    { "releasekey", xpai_AI_releasekey, METH_VARARGS,
      "releasekey(int)->null"},

    { "wallbetween", xpai_wallbetween, METH_VARARGS,
      "wallbetween(int, int, int, int)->int"},
    { "wallbetween_x", xpai_wallbetween, METH_VARARGS,
      "wallbetween_x(int, int, int, int)->int"},
    { "wallbetween_y", xpai_wallbetween, METH_VARARGS,
      "wallbetween_y(int, int, int, int)->int"},

    { "map_get", xpai_map_get, METH_VARARGS,
      "map_get(int, int)->int"},
    { "map_set", xpai_map_set, METH_VARARGS,
      "map_set(int, int, int)->null"},

    { "tomap", xpai_tomap, METH_VARARGS,
      "tomap(int)->int"},
    { "frmap", xpai_frmap, METH_VARARGS,
      "frmap(int)->int"},

    { "msg_body", xpai_AImsg_body, METH_VARARGS, 
      "command(int)->string"},
    { "msg_to", xpai_AImsg_to, METH_VARARGS, 
      "command(int)->string"},
    { "msg_from", xpai_AImsg_from, METH_VARARGS,
      "command(int)->string"},


    { "anglediff", xpai_anglediff, METH_VARARGS, 
      "anglediff(double, double)->double"},
    { "angleadd", xpai_angleadd, METH_VARARGS, 
      "angleadd(double, double)->double"},

    { "rad", xpai_rad, METH_VARARGS, 
      "rad(int)->double"},
    { "deg", xpai_deg, METH_VARARGS, 
      "deg(double)->int"},

    { "set_AImain", xpai_set_AImain, METH_VARARGS, 
      "set_AImain(int)->null"},
    { "call_AImain", xpai_call_AImain, METH_VARARGS, 
      "call_AImain()->null"},
	  
    {NULL,NULL}
};



void AImain (void) {
	PyEval_CallObject(AImain_callback, NULL);
	if (PyErr_Occurred() != NULL)
		PyErr_Print();
	
	return;
}


extern void initxpai(void)
{
     Py_InitModule4(
            "xpai",   // name of the module
            xpaiMethods,  // name of the method table
            "Quake2AI", // doc string for module
            0,   // last two never change
            PYTHON_API_VERSION);
    return;
}

