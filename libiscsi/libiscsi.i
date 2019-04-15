/*
   Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation; either version 2.1 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License
   along with this program; if not, see <http://www.gnu.org/licenses/>.
*/

%module libiscsi

%{
#include <iscsi/iscsi.h>
#include <iscsi/scsi-lowlevel.h>
%}

%include <stdint.i>

%typemap(in) (int cdb_size, unsigned char *cdb)
  (int res, Py_ssize_t size = 0, const void *buf = 0) {
  res = PyObject_AsReadBuffer($input, &buf, &size);
  if (res<0) {
    PyErr_Clear();
    %argument_fail(res, "(TYPEMAP, SIZE)", $symname, $argnum);
  }
  $2 = ($2_ltype) buf;
  $1 = ($1_ltype) (size/sizeof($*2_type));
}

%typemap(in) (int len, unsigned char *rw)
  (int res, Py_ssize_t size = 0, void *buf = 0) {
  res = PyObject_AsWriteBuffer($input, &buf, &size);
  if (res<0) {
    PyErr_Clear();
    %argument_fail(res, "(TYPEMAP, SIZE)", $symname, $argnum);
  }
  $2 = ($2_ltype) buf;
  $1 = ($1_ltype) (size/sizeof($*2_type));
}

%typemap(in) (int len, unsigned char *ro)
  (int res, Py_ssize_t size = 0, const void *buf = 0) {
  res = PyObject_AsReadBuffer($input, &buf, &size);
  if (res<0) {
    PyErr_Clear();
    %argument_fail(res, "(TYPEMAP, SIZE)", $symname, $argnum);
  }
  $2 = ($2_ltype) buf;
  $1 = ($1_ltype) (size/sizeof($*2_type));
}

%apply (int len, unsigned char *ro) { (int len, unsigned char *buf) }

%typemap(in) (unsigned char *ro, uint32_t len)
  (int res, Py_ssize_t size = 0, const void *buf = 0) {
  res = PyObject_AsReadBuffer($input, &buf, &size);
  if (res<0) {
    PyErr_Clear();
    %argument_fail(res, "(TYPEMAP, SIZE)", $symname, $argnum);
  }
  $1 = ($1_ltype) buf;
  $2 = ($2_ltype) (size/sizeof($1_type));
}

%apply (unsigned char *ro, uint32_t len) { (unsigned char *data, uint32_t datalen), (unsigned char *data, int len) }

/* EXTERN int scsi_task_get_status(struct scsi_task *task, struct scsi_sense *sense); */
/* EXTERN void scsi_parse_sense_data(struct scsi_sense *sense, const uint8_t *sb);  */

%typemap(in, numinputs=0) struct scsi_sense *sense (struct scsi_sense *_global_sense) {
  _global_sense = (struct scsi_sense *)calloc(1, sizeof(struct scsi_sense));
  $1 = _global_sense;
}

%typemap(argout) struct scsi_sense *sense {
  PyObject *senseobj = 0;

  senseobj = SWIG_NewPointerObj(SWIG_as_voidptr(_global_sense), SWIGTYPE_p_scsi_sense, SWIG_POINTER_OWN |  0 );
  $result= SWIG_Python_AppendOutput($result, senseobj);
}

%nodefaultctor iscsi_context;

struct iscsi_context {
  %extend {
    ~iscsi_context() { iscsi_destroy_context($self); };
  }
};

%nodefaultctor iscsi_url;

%inline %{
typedef union {
	struct scsi_readcapacity16 readcapacity16;
} scsi_datain_unmarshalled;
%}

/* Add other structures returned by scsi_datain_unmarshall to the union above. */
%warnfilter(302) scsi_datain_unmarshall;
scsi_datain_unmarshalled *scsi_datain_unmarshall(struct scsi_task *task);

%nodefaultctor scsi_task;
%ignore scsi_task::datain;

%include <iscsi/scsi-lowlevel.h>
%include <iscsi/iscsi.h>

%extend struct iscsi_url {
  ~iscsi_url() { iscsi_destroy_url($self); };
}

%rename(datain) scsi_task::datain;

%extend struct scsi_task {
  ~scsi_task() { scsi_free_scsi_task($self); };
   PyObject *_datain_get() {
    if ($self->datain.data) {
      return PyBytes_FromStringAndSize(%const_cast($self->datain.data, char *), %numeric_cast($self->datain.size, Py_ssize_t));
    } else {
      return SWIG_Py_Void();
    }
  }
  %pythoncode %{
    __swig_getmethods__["datain"] = _libiscsi.scsi_task__datain_get
    if _newclass: datain = _swig_property(_libiscsi.scsi_task__datain_get)
  %}
}
